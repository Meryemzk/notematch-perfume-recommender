from django.shortcuts import render
from perfumes.models import Perfume


def home(request):
    trending = Perfume.objects.order_by('-price')[:6]
    brands = Perfume.objects.exclude(brand='').values_list('brand', flat=True).distinct().order_by('brand')[:12]
    return render(request, "home.html", {"trending": trending, "brands": brands})


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def faq(request):
    return render(request, "pages/faq.html")


def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")
