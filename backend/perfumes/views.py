from django.shortcuts import render
from .models import Perfume


def catalog(request):
    perfumes = Perfume.objects.filter(is_active=True).prefetch_related("moods").order_by("-is_featured", "brand", "name")
    return render(request, "perfumes/catalog.html", {"perfumes": perfumes})
