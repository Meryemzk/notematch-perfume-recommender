from django.shortcuts import render
from perfumes.models import Perfume


def home(request):
    trending = Perfume.objects.order_by('-price')[:6]
    brands = Perfume.objects.exclude(brand='').values_list('brand', flat=True).distinct().order_by('brand')[:12]
    feminine_perfumes = Perfume.objects.filter(gender_category='feminine').order_by('brand', 'name')[:4]
    masculine_perfumes = Perfume.objects.filter(gender_category='masculine').order_by('brand', 'name')[:4]
    unisex_perfumes = Perfume.objects.filter(gender_category='unisex').order_by('brand', 'name')[:4]
    return render(request, "home.html", {
        "trending": trending,
        "brands": brands,
        "feminine_perfumes": feminine_perfumes,
        "masculine_perfumes": masculine_perfumes,
        "unisex_perfumes": unisex_perfumes,
    })


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
