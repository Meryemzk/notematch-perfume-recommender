from collections import Counter
from decimal import Decimal
from django.shortcuts import render, redirect

from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer, PRICE_RANGE_CHOICES
from perfumes.models import Perfume


def _price_bounds(price_range):
    return {
        "under_80": (None, Decimal("80.00")),
        "80_120": (Decimal("80.00"), Decimal("120.00")),
        "120_160": (Decimal("120.00"), Decimal("160.00")),
        "160_plus": (Decimal("160.00"), None),
    }.get(price_range, (None, None))


def _apply_price_filter(queryset, price_range):
    low, high = _price_bounds(price_range)
    if low is not None:
        queryset = queryset.filter(price__gte=low)
    if high is not None:
        queryset = queryset.filter(price__lte=high)
    return queryset


def quiz(request):
    questions = SurveyQuestion.objects.prefetch_related("options").all().order_by("order")
    perfumes = Perfume.objects.all().order_by("brand", "name")

    if not questions.exists():
        return render(request, "survey/quiz.html", {
            "questions": questions,
            "perfumes": perfumes,
            "price_ranges": PRICE_RANGE_CHOICES,
            "no_questions": True,
        })

    if request.method == "POST":
        submission = SurveySubmission.objects.create(
            user=request.user if request.user.is_authenticated else None
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
                    "perfumes": perfumes,
                    "price_ranges": PRICE_RANGE_CHOICES,
                    "error": "Please answer all questions."
                })

            opt = SurveyOption.objects.filter(id=picked_option_id, question=q).first()
            if not opt:
                submission.delete()
                return render(request, "survey/quiz.html", {
                    "questions": questions,
                    "perfumes": perfumes,
                    "price_ranges": PRICE_RANGE_CHOICES,
                    "error": "Invalid selection. Please try again."
                })

            SurveyAnswer.objects.create(submission=submission, question=q, option=opt)
            total_energic += opt.energic_points
            total_relax += opt.relax_points

            if opt.note_tag:
                tags.append(opt.note_tag.strip().lower())

        mood_name = "Energic" if total_energic >= total_relax else "Relaxation"
        mood, _ = Mood.objects.get_or_create(name=mood_name)
        top_tags = [t for t, _count in Counter(tags).most_common(3)]

        favourite_ids = []
        for field_name in ["favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3"]:
            value = request.POST.get(field_name)
            if value and value not in favourite_ids:
                favourite_ids.append(value)

        favourites = list(Perfume.objects.filter(id__in=favourite_ids))
        price_range = request.POST.get("price_range") or "any"
        valid_ranges = {value for value, _label in PRICE_RANGE_CHOICES}
        if price_range not in valid_ranges:
            price_range = "any"

        submission.total_energic = total_energic
        submission.total_relax = total_relax
        submission.result_mood = mood
        submission.top_note_tags = ",".join(top_tags)
        submission.price_range = price_range
        if len(favourites) > 0:
            submission.favourite_perfume_1 = favourites[0]
        if len(favourites) > 1:
            submission.favourite_perfume_2 = favourites[1]
        if len(favourites) > 2:
            submission.favourite_perfume_3 = favourites[2]
        submission.save()

        request.session["latest_submission_id"] = submission.id
        request.session["quiz_profile"] = {
            "gender_style": request.POST.get("gender_style", "unisex"),
            "age_range": request.POST.get("age_range", ""),
            "season": request.POST.get("season", ""),
            "weather": request.POST.get("weather", ""),
            "occasion": request.POST.get("occasion", ""),
            "intensity": request.POST.get("intensity", "moderate"),
            "longevity": request.POST.get("longevity", "medium"),
            "preferred_notes": request.POST.getlist("preferred_notes"),
            "disliked_notes": request.POST.getlist("disliked_notes"),
            "favourite_brands": request.POST.get("favourite_brands", ""),
            "already_like": request.POST.get("already_like", ""),
            "personality": request.POST.get("personality", "elegant"),
            "lifestyle": request.POST.get("lifestyle", ""),
        }
        return redirect("quiz_result")

    return render(request, "survey/quiz.html", {
        "questions": questions,
        "perfumes": perfumes,
        "price_ranges": PRICE_RANGE_CHOICES,
    })


def result(request):
    latest = None
    latest_id = request.session.get("latest_submission_id")

    if latest_id:
        latest = (
            SurveySubmission.objects
            .select_related("result_mood", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3")
            .filter(id=latest_id)
            .first()
        )

    if not latest and request.user.is_authenticated:
        latest = (
            SurveySubmission.objects
            .filter(user=request.user)
            .select_related("result_mood", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3")
            .order_by("-created_at")
            .first()
        )

    if not latest:
        return redirect("quiz")

    perfumes = Perfume.objects.filter(moods=latest.result_mood).distinct()
    price_filtered_perfumes = _apply_price_filter(perfumes, latest.price_range)
    if price_filtered_perfumes.exists():
        perfumes = price_filtered_perfumes

    tags = [t.strip().lower() for t in (latest.top_note_tags or "").split(",") if t.strip()]
    favourite_perfumes = latest.favourite_perfumes
    favourite_scents = []
    favourite_brands = []
    for favourite in favourite_perfumes:
        favourite_brands.append((favourite.brand or "").lower())
        favourite_scents.extend([favourite.scent_1, favourite.scent_2, favourite.scent_3])

    ranked_perfumes = []
    for perfume in perfumes:
        score = 5
        notes_text = perfume.searchable_notes
        matched_tags = []
        reasons = []

        for tag in tags:
            if tag in notes_text:
                score += 3
                matched_tags.append(tag)
                reasons.append(f"matches your {tag} preference")

        for fav_scent in favourite_scents:
            if fav_scent and fav_scent in notes_text:
                score += 2

        if perfume.brand and perfume.brand.lower() in favourite_brands:
            score += 2
            reasons.append(f"similar brand style to your favourites")

        if latest.price_range != "any":
            score += 1
            reasons.append("fits your selected price range")

        profile = request.session.get("quiz_profile", {})
        profile_notes = profile.get("preferred_notes", []) or []
        disliked_notes = profile.get("disliked_notes", []) or []
        perfume_notes = {perfume.scent_1, perfume.scent_2, perfume.scent_3}
        for note in profile_notes:
            if note in perfume_notes or note in notes_text:
                score += 4
                matched_tags.append(note)
                reasons.append(f"reflects your love of {note} notes")
        for note in disliked_notes:
            if note in perfume_notes or note in notes_text:
                score -= 5
                reasons.append(f"contains a note you may dislike: {note}")
        if profile.get("season") in ["winter", "autumn"] and perfume_notes & {"amber", "vanilla", "woody", "oud", "leather", "spicy"}:
            score += 4
            reasons.append("suits colder London weather")
        if profile.get("season") in ["summer", "spring"] and perfume_notes & {"fresh", "citrus", "aquatic", "green", "floral"}:
            score += 4
            reasons.append("suits lighter London seasons")
        if profile.get("weather") == "rainy" and perfume_notes & {"musk", "woody", "amber", "green"}:
            score += 3
            reasons.append("works well on rainy London days")
        if profile.get("occasion") in ["luxury", "date", "formal", "wedding"] and (perfume.price >= 75 or perfume_notes & {"amber", "oud", "leather", "jasmine"}):
            score += 3
            reasons.append("feels polished for your London occasion")
        if profile.get("intensity") == "strong" and perfume_notes & {"amber", "oud", "leather", "spicy", "oriental"}:
            score += 3
            reasons.append("has the stronger presence you requested")
        if profile.get("intensity") == "subtle" and perfume_notes & {"fresh", "musk", "citrus", "aquatic"}:
            score += 3
            reasons.append("keeps the profile subtle and refined")
        favourite_brand_text = (profile.get("favourite_brands") or "").lower()
        if perfume.brand and perfume.brand.lower() in favourite_brand_text:
            score += 4
            reasons.append("matches a brand you mentioned")
        match_percent = max(55, min(99, int(score * 6)))
        london_price = f"£{perfume.price}"
        ranked_perfumes.append({
            "perfume": perfume,
            "score": score,
            "match_percent": match_percent,
            "matched_tags": sorted(set(matched_tags)),
            "reasons": list(dict.fromkeys(reasons))[:4] or ["balanced match for your stated scent profile"],
            "strengths": ["Elegant scent profile", "Good London availability", "Versatile day-to-evening use"][:2],
            "weaknesses": ["May project strongly in small offices"] if profile.get("intensity") == "subtle" else ["Premium price point" if perfume.price >= 140 else "May need reapplying after commuting"],
            "season": profile.get("season", "all-year") or "all-year",
            "occasion": profile.get("occasion", "daily wear") or "daily wear",
            "longevity": "Strong" if perfume_notes & {"amber", "oud", "leather", "spicy"} else "Moderate",
            "projection": "Noticeable" if perfume_notes & {"amber", "oud", "leather", "spicy"} else "Close-to-skin",
            "london_price": london_price,
        })

    ranked_perfumes.sort(key=lambda x: (x["score"], -float(x["perfume"].price or 0)), reverse=True)
    top_recommendations = ranked_perfumes[:6]

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "top_recommendations": top_recommendations,
        "favourite_perfumes": favourite_perfumes,
        "price_range_label": dict(PRICE_RANGE_CHOICES).get(latest.price_range, "Any price"),
        "quiz_profile": request.session.get("quiz_profile", {}),
    })
