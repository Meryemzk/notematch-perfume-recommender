from django.shortcuts import render
from .models import Perfume

def catalog(request):
    perfumes = Perfume.objects.all().order_by("name")
    return render(request, "perfumes/catalog.html", {"perfumes": perfumes})
