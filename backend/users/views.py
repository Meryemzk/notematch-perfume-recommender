from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from survey.models import SurveySubmission, UserPreferenceProfile


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    latest = (
        SurveySubmission.objects
        .filter(user=request.user)
        .select_related("result_mood")
        .order_by("-created_at")[:10]
    )
    saved_profile = UserPreferenceProfile.objects.filter(user=request.user).first()
    return render(request, "users/profile.html", {"latest": latest, "saved_profile": saved_profile})


@login_required
def edit_preferences(request):
    saved_profile = UserPreferenceProfile.objects.filter(user=request.user).first()
    choices = {
        "gender": UserPreferenceProfile.GENDER_PREFERENCE_CHOICES,
        "style": UserPreferenceProfile.STYLE_PREFERENCE_CHOICES,
        "budget": UserPreferenceProfile.BUDGET_CHOICES,
    }

    if request.method == "POST":
        values = {
            "favourite_perfume_1": (request.POST.get("favourite_perfume_1") or "").strip(),
            "favourite_perfume_2": (request.POST.get("favourite_perfume_2") or "").strip(),
            "favourite_perfume_3": (request.POST.get("favourite_perfume_3") or "").strip(),
            "preferred_gender": request.POST.get("preferred_gender") or "no_preference",
            "style_preference": request.POST.get("style_preference") or "both",
            "budget_range": request.POST.get("budget_range") or "no_preference",
        }
        if not all([values["favourite_perfume_1"], values["favourite_perfume_2"], values["favourite_perfume_3"]]):
            messages.error(request, "Please enter three favourite perfumes.")
        else:
            if saved_profile is None:
                UserPreferenceProfile.objects.create(user=request.user, **values)
            else:
                for key, value in values.items():
                    setattr(saved_profile, key, value)
                saved_profile.save()
            messages.success(request, "Your saved preference profile has been updated.")
            return redirect("profile")

    return render(request, "users/edit_preferences.html", {"saved_profile": saved_profile, "choices": choices})
