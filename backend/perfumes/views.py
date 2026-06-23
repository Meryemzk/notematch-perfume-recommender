from decimal import Decimal
from django.db.models import Q
from django.shortcuts import render
from .models import Perfume

PRICE_RANGES = [
    ("any", "Any price"),
    ("under_80", "Under £80"),
    ("80_120", "£80 - £120"),
    ("120_160", "£120 - £160"),
    ("160_plus", "£160+"),
]


def _apply_price_filter(queryset, selected_price):
    if selected_price == "under_80":
        return queryset.filter(price__lte=Decimal("80.00"))
    if selected_price == "80_120":
        return queryset.filter(price__gte=Decimal("80.00"), price__lte=Decimal("120.00"))
    if selected_price == "120_160":
        return queryset.filter(price__gte=Decimal("120.00"), price__lte=Decimal("160.00"))
    if selected_price == "160_plus":
        return queryset.filter(price__gte=Decimal("160.00"))
    return queryset


def catalog(request):
    query = request.GET.get("q", "").strip()
    selected_price = request.GET.get("price", "any")
    if selected_price not in {value for value, _label in PRICE_RANGES}:
        selected_price = "any"

    perfumes = Perfume.objects.all().order_by("brand", "name")
    if query:
        perfumes = perfumes.filter(Q(name__icontains=query) | Q(brand__icontains=query) | Q(notes__icontains=query))
    perfumes = _apply_price_filter(perfumes, selected_price)

    return render(request, "perfumes/catalog.html", {
        "perfumes": perfumes,
        "query": query,
        "price_ranges": PRICE_RANGES,
        "selected_price": selected_price,
    })
