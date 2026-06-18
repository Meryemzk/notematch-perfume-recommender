from collections import Counter
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer
from perfumes.models import Perfume


COMMON_NOTE_TAGS = [
    "citrus", "fresh", "lavender", "vanilla", "rose", "floral", "musk",
    "woody", "cedar", "sandalwood", "amber", "spicy", "pepper", "bergamot",
]


def _budget_bounds(budget_range):
    """Return min/max price bounds for the stored budget value."""
    bounds = {
        "under_30": (Decimal("0"), Decimal("30")),
        "30_60": (Decimal("30"), Decimal("60")),
        "60_100": (Decimal("60"), Decimal("100")),
        "over_100": (Decimal("100"), None),
    }
    return bounds.get(budget_range, (None, None))


def _extract_tags_from_favourites(favourite_names):
    """
    Find entered favourite perfumes in the catalogue and reuse their notes as preference tags.
    If the name is not in the catalogue, this safely returns no tags for that perfume.
    """
    tags = []
    for name in favourite_names:
        name = (name or "").strip()
        if not name:
            continue

        matches = Perfume.objects.filter(name__icontains=name)[:3]
        for perfume in matches:
            notes_text = (perfume.notes or "").lower()
            for tag in COMMON_NOTE_TAGS:
                if tag in notes_text:
                    tags.append(tag)
    return tags


@login_required
def quiz(request):
    questions = SurveyQuestion.objects.all().order_by("order")

    preference_choices = {
        "gender": SurveySubmission.GENDER_PREFERENCE_CHOICES,
        "style": SurveySubmission.STYLE_PREFERENCE_CHOICES,
        "budget": SurveySubmission.BUDGET_CHOICES,
    }

    if not questions.exists():
        return render(request, "survey/quiz.html", {
            "questions": questions,
            "no_questions": True,
            "preference_choices": preference_choices,
        })

    if request.method == "POST":
        favourite_1 = (request.POST.get("favourite_perfume_1") or "").strip()
        favourite_2 = (request.POST.get("favourite_perfume_2") or "").strip()
        favourite_3 = (request.POST.get("favourite_perfume_3") or "").strip()
        preferred_gender = request.POST.get("preferred_gender") or "no_preference"
        style_preference = request.POST.get("style_preference") or "both"
        budget_range = request.POST.get("budget_range") or "no_preference"

        valid_gender_values = [choice[0] for choice in SurveySubmission.GENDER_PREFERENCE_CHOICES]
        valid_style_values = [choice[0] for choice in SurveySubmission.STYLE_PREFERENCE_CHOICES]
        valid_budget_values = [choice[0] for choice in SurveySubmission.BUDGET_CHOICES]

        if not all([favourite_1, favourite_2, favourite_3]):
            return render(request, "survey/quiz.html", {
                "questions": questions,
                "preference_choices": preference_choices,
                "error": "Please enter three favourite perfumes so the system can learn your past preferences.",
                "form_values": request.POST,
            })

        if preferred_gender not in valid_gender_values or style_preference not in valid_style_values or budget_range not in valid_budget_values:
            return render(request, "survey/quiz.html", {
                "questions": questions,
                "preference_choices": preference_choices,
                "error": "Invalid preference selection. Please try again.",
                "form_values": request.POST,
            })

        submission = SurveySubmission.objects.create(
            user=request.user,
            favourite_perfume_1=favourite_1,
            favourite_perfume_2=favourite_2,
            favourite_perfume_3=favourite_3,
            preferred_gender=preferred_gender,
            style_preference=style_preference,
            budget_range=budget_range,
        )

        total_energic = 0
        total_relax = 0
        tags = []

        for q in questions:
            picked_option_id = request.POST.get(f"q_{q.id}")
            if not picked_option_id:
                submission.delete()
                return render(request, "survey/quiz.html", {
                    "questions": questions,
                    "preference_choices": preference_choices,
                    "error": "Please answer all mood and scent questions.",
                    "form_values": request.POST,
                })

            opt = SurveyOption.objects.filter(id=picked_option_id, question=q).first()
            if not opt:
                submission.delete()
                return render(request, "survey/quiz.html", {
                    "questions": questions,
                    "preference_choices": preference_choices,
                    "error": "Invalid selection. Please try again.",
                    "form_values": request.POST,
                })

            SurveyAnswer.objects.create(submission=submission, question=q, option=opt)

            total_energic += opt.energic_points
            total_relax += opt.relax_points

            if opt.note_tag:
                tags.append(opt.note_tag.strip().lower())

        favourite_tags = _extract_tags_from_favourites([favourite_1, favourite_2, favourite_3])
        tags.extend(favourite_tags)

        mood_name = "Energic" if total_energic >= total_relax else "Relaxation"
        mood, _ = Mood.objects.get_or_create(name=mood_name)

        top_tags = [t for t, _count in Counter(tags).most_common(5)]

        submission.total_energic = total_energic
        submission.total_relax = total_relax
        submission.result_mood = mood
        submission.top_note_tags = ",".join(top_tags)
        submission.save()

        return redirect("quiz_result")

    return render(request, "survey/quiz.html", {
        "questions": questions,
        "preference_choices": preference_choices,
    })


@login_required
def result(request):
    latest = (
        SurveySubmission.objects
        .filter(user=request.user)
        .select_related("result_mood")
        .order_by("-created_at")
        .first()
    )

    if not latest:
        return redirect("quiz")

    perfumes = Perfume.objects.filter(moods=latest.result_mood).distinct()

    tags = [t.strip().lower() for t in (latest.top_note_tags or "").split(",") if t.strip()]
    favourite_names = [
        latest.favourite_perfume_1,
        latest.favourite_perfume_2,
        latest.favourite_perfume_3,
    ]

    min_price, max_price = _budget_bounds(latest.budget_range)

    ranked_perfumes = []

    for perfume in perfumes:
        score = 0
        reasons = []
        notes_text = (perfume.notes or "").lower()

        # Base score for matching mood
        score += 5
        reasons.append(f"matches your {latest.result_mood.name} mood")

        # Extra score for matching note tags from quiz and favourite perfumes
        matched_tags = []
        for tag in tags:
            if tag in notes_text and tag not in matched_tags:
                score += 3
                matched_tags.append(tag)
        if matched_tags:
            reasons.append("shares preferred notes: " + ", ".join(matched_tags))

        # Gender preference scoring
        if latest.preferred_gender == "no_preference":
            score += 1
        elif perfume.gender_category in [latest.preferred_gender, "unisex"]:
            score += 3
            reasons.append("fits your gender preference")
        else:
            score -= 4

        # New/classic preference scoring
        if latest.style_preference == "both":
            score += 1
        elif perfume.style_category == latest.style_preference:
            score += 3
            reasons.append(f"fits your {latest.get_style_preference_display().lower()} style choice")
        else:
            score -= 2

        # Budget scoring
        if latest.budget_range == "no_preference":
            score += 1
        else:
            price = perfume.price or Decimal("0")
            in_budget = True
            if min_price is not None and price < min_price:
                in_budget = False
            if max_price is not None and price > max_price:
                in_budget = False

            if in_budget:
                score += 3
                reasons.append("fits your budget")
            else:
                score -= 3

        # Avoid recommending the exact same perfumes entered as favourites.
        # Still use them as preference evidence, but recommend alternatives.
        if perfume.name.lower() in [name.lower().strip() for name in favourite_names if name]:
            score -= 5
            reasons.append("you already listed this as a favourite")

        ranked_perfumes.append({
            "perfume": perfume,
            "score": score,
            "matched_tags": matched_tags,
            "reasons": reasons[:4],
        })

    ranked_perfumes.sort(key=lambda x: x["score"], reverse=True)

    top_recommendations = ranked_perfumes[:4]

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "favourite_names": favourite_names,
        "top_recommendations": top_recommendations,
    })
