from collections import Counter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer
from .seed_data import ensure_starter_content
from perfumes.models import Perfume


@login_required
def quiz(request):
    if not SurveyQuestion.objects.exists():
        ensure_starter_content()

    questions = SurveyQuestion.objects.prefetch_related("options").all().order_by("order")

    if request.method == "POST":
        submission = SurveySubmission.objects.create(user=request.user)

        total_energic = 0
        total_relax = 0
        tags = []
        mood_votes = []

        for q in questions:
            picked_option_id = request.POST.get(f"q_{q.id}")
            if not picked_option_id:
                submission.delete()
                messages.error(request, "Please answer every survey question before submitting.")
                return render(request, "survey/quiz.html", {"questions": questions})

            opt = SurveyOption.objects.filter(id=picked_option_id, question=q).first()
            if not opt:
                submission.delete()
                messages.error(request, "One answer was invalid. Please try the survey again.")
                return render(request, "survey/quiz.html", {"questions": questions})

            SurveyAnswer.objects.create(submission=submission, question=q, option=opt)

            total_energic += opt.energic_points
            total_relax += opt.relax_points

            if opt.note_tag:
                tags.append(opt.note_tag.strip().lower())
            if opt.target_mood:
                mood_votes.append(opt.target_mood.strip())

        top_tags = [t for t, _count in Counter(tags).most_common(4)]

        if mood_votes:
            mood_name = Counter(mood_votes).most_common(1)[0][0]
        else:
            mood_name = "Energic" if total_energic >= total_relax else "Relaxation"

        mood, _ = Mood.objects.get_or_create(name=mood_name)

        submission.total_energic = total_energic
        submission.total_relax = total_relax
        submission.result_mood = mood
        submission.top_note_tags = ",".join(top_tags)
        submission.save()

        messages.success(request, "Survey completed. Your personalized perfume matches are ready.")
        return redirect("quiz_result")

    return render(request, "survey/quiz.html", {"questions": questions})


@login_required
def result(request):
    if not Perfume.objects.exists() or not SurveyQuestion.objects.exists():
        ensure_starter_content()

    latest = (
        SurveySubmission.objects
        .filter(user=request.user)
        .select_related("result_mood")
        .order_by("-created_at")
        .first()
    )

    if not latest:
        messages.info(request, "Please complete the survey first so we can recommend perfumes.")
        return redirect("quiz")

    tags = [t.strip().lower() for t in (latest.top_note_tags or "").split(",") if t.strip()]
    all_perfumes = Perfume.objects.prefetch_related("moods").all()

    ranked_perfumes = []
    for perfume in all_perfumes:
        score = 0
        notes_text = (perfume.notes or "").lower()
        mood_names = [m.name for m in perfume.moods.all()]

        if latest.result_mood and latest.result_mood.name in mood_names:
            score += 6

        matched_tags = []
        for tag in tags:
            if tag and tag in notes_text:
                score += 3
                matched_tags.append(tag)

        if score > 0:
            ranked_perfumes.append({
                "perfume": perfume,
                "score": score,
                "matched_tags": matched_tags,
                "moods": mood_names,
            })

    ranked_perfumes.sort(key=lambda x: x["score"], reverse=True)
    top_recommendations = ranked_perfumes[:6]

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "top_recommendations": top_recommendations,
    })
