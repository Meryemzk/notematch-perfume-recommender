from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import SurveyQuestion, SurveySubmission, UserPreferenceProfile
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

    if not questions.exists():
        return render(request, "survey/quiz.html", {
            "questions": questions,
            "no_questions": True,
            "preference_choices": preference_choices,
            "saved_profile": saved_profile,
            "profile_values": _profile_values(saved_profile),
        })

    if request.method == "POST":
        profile, error = get_or_create_profile_from_post(request.user, request.POST)
        if error:
            return render(request, "survey/quiz.html", {
                "questions": questions,
                "preference_choices": preference_choices,
                "saved_profile": saved_profile,
                "profile_values": _profile_values(saved_profile),
                "error": error,
                "form_values": request.POST,
            })

        submission = SurveySubmission.objects.create(
            user=request.user,
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
            return render(request, "survey/quiz.html", {
                "questions": questions,
                "preference_choices": preference_choices,
                "saved_profile": saved_profile,
                "profile_values": _profile_values(saved_profile),
                "error": error,
                "form_values": request.POST,
            })

        if request.POST.get("update_saved_profile") == "yes":
            messages.success(request, "Your saved perfume profile has been updated.")
        return redirect("quiz_result")

    return render(request, "survey/quiz.html", {
        "questions": questions,
        "preference_choices": preference_choices,
        "saved_profile": saved_profile,
        "profile_values": _profile_values(saved_profile),
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

    ranked_perfumes, tags = rank_perfumes_for_submission(latest)
    top_recommendations = ranked_perfumes[:8]

    return render(request, "survey/result.html", {
        "latest": latest,
        "tags": tags,
        "favourite_names": latest.favourite_names,
        "top_recommendations": top_recommendations,
    })
