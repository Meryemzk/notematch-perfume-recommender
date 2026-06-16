from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from survey.models import SurveySubmission
from perfumes.models import Perfume


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are already signed in as {request.user.username}.")
        return redirect("home")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}. You are now signed in.")
            return redirect(request.GET.get("next") or "home")
        messages.error(request, "Login failed. Please check your username and password.")

    return render(request, "registration/login.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You already have an active account session.")
        return redirect("profile")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}. Your NoteMatch account was created successfully.")
            return redirect("profile")
        messages.error(request, "Sign up failed. Please correct the highlighted errors.")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    submissions = (
        SurveySubmission.objects
        .filter(user=request.user)
        .select_related("result_mood")
        .order_by("-created_at")[:10]
    )
    total_surveys = SurveySubmission.objects.filter(user=request.user).count()
    favorite_mood = submissions[0].result_mood.name if submissions and submissions[0].result_mood else "Not discovered yet"
    perfume_count = Perfume.objects.count()

    return render(request, "users/profile.html", {
        "latest": submissions,
        "total_surveys": total_surveys,
        "favorite_mood": favorite_mood,
        "perfume_count": perfume_count,
    })
