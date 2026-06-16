from collections import Counter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer
from perfumes.models import Perfume


@login_required
def quiz(request):
    questions = SurveyQuestion.objects.all().order_by("order")

    if not questions.exists():
        return render(request, "survey/quiz.html", {
            "questions": questions,
            "no_questions": True,
        })

    if request.method == "POST":
        submission = SurveySubmission.objects.create(user=request.user)

        total_energic = 0
        total_relax = 0
        tags = []

        for q in questions:
            picked_option_id = request.POST.get(f"q_{q.id}")
            if not picked_option_id:
                return render(request, "survey/quiz.html", {
                    "questions": questions,
                    "error": "Please answer all questions."
                })

            opt = SurveyOption.objects.filter(id=picked_option_id, question=q).first()
            if not opt:
                return render(request, "survey/quiz.html", {
                    "questions": questions,
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

        submission.total_energic = total_energic
        submission.total_relax = total_relax
        submission.result_mood = mood
        submission.top_note_tags = ",".join(top_tags)
        submission.save()

        return redirect("quiz_result")

    return render(request, "survey/quiz.html", {"questions": questions})


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

    ranked_perfumes = []

    for perfume in perfumes:
        score = 0
        notes_text = (perfume.notes or "").lower()

        # Base score for matching mood
        score += 5

        # Extra score for matching note tags
        matched_tags = []
        for tag in tags:
            if tag in notes_text:
                score += 3
                matched_tags.append(tag)

        ranked_perfumes.append({
            "perfume": perfume,
            "score": score,
            "matched_tags": matched_tags,
        })

    ranked_perfumes.sort(key=lambda x: x["score"], reverse=True)

    top_recommendations = ranked_perfumes[:4]

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "top_recommendations": top_recommendations,
    })