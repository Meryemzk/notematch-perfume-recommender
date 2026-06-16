from django.shortcuts import render
from perfumes.models import Perfume
from survey.models import SurveyQuestion
from survey.seed_data import ensure_starter_content


def home(request):
    if not Perfume.objects.exists() or not SurveyQuestion.objects.exists():
        ensure_starter_content()

    featured_perfumes = Perfume.objects.prefetch_related("moods").all()[:6]
    return render(request, "home.html", {"featured_perfumes": featured_perfumes})
