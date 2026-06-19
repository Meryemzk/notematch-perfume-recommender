from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import SurveyQuestion, SurveySubmission, UserPreferenceProfile, RecommendationFeedback
from .services import get_or_create_profile_from_post, create_mood_result, rank_perfumes_for_submission


def _preference_choices():
    return {
        "gender": UserPreferenceProfile.GENDER_PREFERENCE_CHOICES,
        "style": UserPreferenceProfile.STYLE_PREFERENCE_CHOICES,
        "budget": UserPreferenceProfile.BUDGET_CHOICES,
    }


def _profile_values(profile):
    if not profile:
        return {
            "favourite_perfume_1": "",
            "favourite_perfume_2": "",
            "favourite_perfume_3": "",
            "preferred_gender": "no_preference",
            "style_preference": "both",
            "budget_range": "no_preference",
        }
    return {
        "favourite_perfume_1": profile.favourite_perfume_1,
        "favourite_perfume_2": profile.favourite_perfume_2,
        "favourite_perfume_3": profile.favourite_perfume_3,
        "preferred_gender": profile.preferred_gender,
        "style_preference": profile.style_preference,
        "budget_range": profile.budget_range,
    }


@login_required
def quiz(request):
    questions = SurveyQuestion.objects.filter(is_active=True).order_by("order")
    saved_profile = UserPreferenceProfile.objects.filter(user=request.user).first()
    preference_choices = _preference_choices()

    context = {
        "questions": questions,
        "preference_choices": preference_choices,
        "saved_profile": saved_profile,
        "profile_values": _profile_values(saved_profile),
    }

    if not questions.exists():
        context["no_questions"] = True
        return render(request, "survey/quiz.html", context)

    if request.method == "POST":
        if not (request.POST.get("age_confirmed") == "yes" and request.POST.get("consent_given") == "yes" and request.POST.get("privacy_acknowledged") == "yes"):
            context.update({
                "error": "Please confirm age, consent and privacy acknowledgement before continuing.",
                "form_values": request.POST,
            })
            return render(request, "survey/quiz.html", context)

        profile, error = get_or_create_profile_from_post(request.user, request.POST)
        if error:
            context.update({"error": error, "form_values": request.POST})
            return render(request, "survey/quiz.html", context)

        submission = SurveySubmission.objects.create(
            user=request.user,
            age_confirmed=True,
            consent_given=True,
            privacy_acknowledged=True,
            favourite_perfume_1=profile.favourite_perfume_1,
            favourite_perfume_2=profile.favourite_perfume_2,
            favourite_perfume_3=profile.favourite_perfume_3,
            preferred_gender=profile.preferred_gender,
            style_preference=profile.style_preference,
            budget_range=profile.budget_range,
        )

        error = create_mood_result(submission, questions, request.POST, profile)
        if error:
            submission.delete()
            context.update({"error": error, "form_values": request.POST})
            return render(request, "survey/quiz.html", context)

        if request.POST.get("update_saved_profile") == "yes":
            messages.success(request, "Your saved perfume profile has been updated.")
        return redirect("quiz_result")

    return render(request, "survey/quiz.html", context)


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

    if request.method == "POST":
        was_useful = request.POST.get("was_useful") == "yes"
        try:
            rating = int(request.POST.get("rating", "5"))
        except ValueError:
            rating = 5
        rating = max(1, min(5, rating))
        comment = (request.POST.get("comment") or "").strip()
        RecommendationFeedback.objects.update_or_create(
            submission=latest,
            defaults={
                "user": request.user,
                "was_useful": was_useful,
                "rating": rating,
                "comment": comment,
            },
        )
        messages.success(request, "Thank you. Your feedback has been saved and can support future system improvement.")
        return redirect("quiz_result")

    ranked_perfumes, tags = rank_perfumes_for_submission(latest)
    top_recommendations = ranked_perfumes[:8]
    existing_feedback = getattr(latest, "feedback", None)

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "favourite_names": latest.favourite_names,
        "top_recommendations": top_recommendations,
        "existing_feedback": existing_feedback,
    })
