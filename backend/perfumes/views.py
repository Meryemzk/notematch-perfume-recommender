from django.db.models import Q
from django.shortcuts import render
from .models import Perfume
from survey.seed_data import ensure_starter_content


def catalog(request):
    if not Perfume.objects.exists():
        ensure_starter_content()

    query = request.GET.get("q", "").strip()
    mood = request.GET.get("mood", "").strip()
    brand = request.GET.get("brand", "").strip()

    perfumes = Perfume.objects.prefetch_related("moods").all()

    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(notes__icontains=query)
            | Q(description__icontains=query)
            | Q(best_for__icontains=query)
            | Q(boosts_mood__icontains=query)
        )

    if mood:
        perfumes = perfumes.filter(moods__name__iexact=mood)

    if brand:
        perfumes = perfumes.filter(brand__iexact=brand)

    perfumes = perfumes.distinct().order_by("brand", "name")

    all_perfumes = Perfume.objects.prefetch_related("moods").all()
    brands = sorted({p.brand for p in all_perfumes if p.brand})
    moods = sorted({m.name for p in all_perfumes for m in p.moods.all()})

    return render(request, "perfumes/catalog.html", {
        "perfumes": perfumes,
        "brands": brands,
        "moods": moods,
        "query": query,
        "selected_mood": mood,
        "selected_brand": brand,
    })
