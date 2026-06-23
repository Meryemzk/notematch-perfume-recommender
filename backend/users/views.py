from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from survey.models import SurveySubmission
from .forms import NoteMatchSignUpForm


def signup(request):
    if request.method == "POST":
        form = NoteMatchSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = NoteMatchSignUpForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    latest = (
        SurveySubmission.objects
        .filter(user=request.user)
        .select_related("result_mood")
        .order_by("-created_at")[:10]
    )
    return render(request, "users/profile.html", {"latest": latest})
