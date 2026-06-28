from decimal import Decimal
from urllib.parse import urlencode
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Perfume, SCENT_CHOICES
from survey.models import SurveySubmission, SurveyOption, SurveyQuestion, Mood
from django.contrib.auth.models import User

PRICE_RANGES = [
    ("any", "Any price"),
    ("under_80", "Under £80"),
    ("80_120", "£80 - £120"),
    ("120_160", "£120 - £160"),
    ("160_plus", "£160+"),
]

LONDON_OCCASIONS = [
    ("office", "Office wear / Canary Wharf"), ("date", "Date night / Soho"),
    ("formal", "Formal event"), ("wedding", "Wedding guest"),
    ("luxury", "Mayfair evening"), ("commute", "Commuting"),
    ("weekend", "Casual weekend"), ("gift", "Gifting"),
]

SEASONS = [("spring", "Spring"), ("summer", "Summer"), ("autumn", "Autumn"), ("winter", "Winter"), ("rainy", "Rainy London days")]
INTENSITIES = [("subtle", "Subtle"), ("moderate", "Moderate"), ("strong", "Strong")]
LONDON_RETAILERS = [
    {"name": "Selfridges", "area": "Oxford Street", "url": "https://www.selfridges.com/GB/en/cat/beauty/fragrance/"},
    {"name": "Harrods", "area": "Knightsbridge", "url": "https://www.harrods.com/en-gb/shopping/beauty/fragrance"},
    {"name": "Liberty London", "area": "Soho", "url": "https://www.libertylondon.com/uk/beauty/fragrance/"},
    {"name": "Space NK", "area": "Chelsea, Covent Garden & London-wide", "url": "https://www.spacenk.com/uk/fragrance"},
    {"name": "John Lewis", "area": "Oxford Street", "url": "https://www.johnlewis.com/browse/beauty/fragrance/_/N-flw"},
    {"name": "The Perfume Shop", "area": "London-wide", "url": "https://www.theperfumeshop.com/"},
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


def _perfume_meta(perfume):
    notes = set([perfume.scent_1, perfume.scent_2, perfume.scent_3])
    warm = bool(notes & {"amber", "vanilla", "oud", "leather", "tobacco", "spicy", "oriental"})
    fresh = bool(notes & {"fresh", "citrus", "aquatic", "green"})
    floral = bool(notes & {"floral", "rose", "jasmine", "powdery"})
    woody = bool(notes & {"woody", "leather", "oud", "tobacco"})
    strong = bool(notes & {"oud", "leather", "amber", "spicy", "tobacco", "oriental"}) or perfume.price >= 140
    season = "Winter" if warm and strong else "Summer" if fresh else "Spring" if floral else "Autumn"
    occasion = "Mayfair evenings" if strong and perfume.price >= 140 else "Canary Wharf office" if fresh else "Soho date nights" if warm or floral else "London weekends"
    return {
        "notes": notes,
        "season": season,
        "occasion": occasion,
        "longevity": 9 if strong else 7 if warm else 6,
        "projection": 9 if strong else 7 if warm else 5,
        "sillage": 8 if strong else 7 if warm else 5,
        "style": "Bold luxury" if strong else "Fresh modern" if fresh else "Elegant classic",
        "gender": "Unisex style" if warm and fresh else "Feminine-leaning" if floral else "Masculine-leaning" if fresh or woody else "Unisex style",
    }


def _filter_london_context(queryset, season, occasion, intensity):
    if season in {"summer", "rainy"}:
        queryset = queryset.filter(Q(scent_1__in=["fresh", "citrus", "aquatic", "green"]) | Q(scent_2__in=["fresh", "citrus", "aquatic", "green"]) | Q(scent_3__in=["fresh", "citrus", "aquatic", "green"]))
    elif season in {"winter", "autumn"}:
        queryset = queryset.filter(Q(scent_1__in=["amber", "vanilla", "woody", "oud", "leather", "spicy"]) | Q(scent_2__in=["amber", "vanilla", "woody", "oud", "leather", "spicy"]) | Q(scent_3__in=["amber", "vanilla", "woody", "oud", "leather", "spicy"]))
    if occasion in {"date", "luxury", "formal", "wedding"}:
        queryset = queryset.filter(price__gte=Decimal("75.00"))
    if intensity == "subtle":
        queryset = queryset.exclude(scent_1__in=["oud", "leather", "tobacco"]).exclude(scent_2__in=["oud", "leather", "tobacco"])
    if intensity == "strong":
        queryset = queryset.filter(Q(scent_1__in=["amber", "oud", "leather", "spicy", "oriental"]) | Q(scent_2__in=["amber", "oud", "leather", "spicy", "oriental"]) | Q(scent_3__in=["amber", "oud", "leather", "spicy", "oriental"]))
    return queryset


def catalog(request):
    query = request.GET.get("q", "").strip()
    selected_price = request.GET.get("price", "any")
    selected_brand = request.GET.get("brand", "").strip()
    selected_note = request.GET.get("note", "").strip()
    selected_season = request.GET.get("season", "").strip()
    selected_occasion = request.GET.get("occasion", "").strip()
    selected_intensity = request.GET.get("intensity", "").strip()
    sort = request.GET.get("sort", "brand")
    view_mode = request.GET.get("view", "grid")

    valid_prices = {value for value, _ in PRICE_RANGES}
    if selected_price not in valid_prices:
        selected_price = "any"

    perfumes = Perfume.objects.all()
    if query:
        perfumes = perfumes.filter(Q(name__icontains=query) | Q(brand__icontains=query) | Q(notes__icontains=query) | Q(scent_1__icontains=query) | Q(scent_2__icontains=query) | Q(scent_3__icontains=query))
    if selected_brand:
        perfumes = perfumes.filter(brand=selected_brand)
    if selected_note:
        perfumes = perfumes.filter(Q(scent_1=selected_note) | Q(scent_2=selected_note) | Q(scent_3=selected_note) | Q(notes__icontains=selected_note))
    perfumes = _apply_price_filter(perfumes, selected_price)
    perfumes = _filter_london_context(perfumes, selected_season, selected_occasion, selected_intensity)

    sort_map = {"price": "price", "price_desc": "-price", "newest": "-id", "rating": "-price", "popularity": "brand", "best": "brand", "brand": "brand", "name": "name"}
    perfumes = perfumes.order_by(sort_map.get(sort, "brand"), "name")

    paginator = Paginator(perfumes, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    brands = Perfume.objects.exclude(brand="").values_list("brand", flat=True).distinct().order_by("brand")
    suggestions = Perfume.objects.values_list("name", flat=True).order_by("name")[:60]

    return render(request, "perfumes/catalog.html", {
        "perfumes": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "price_ranges": PRICE_RANGES,
        "selected_price": selected_price,
        "brands": brands,
        "selected_brand": selected_brand,
        "scent_choices": SCENT_CHOICES,
        "selected_note": selected_note,
        "seasons": SEASONS,
        "selected_season": selected_season,
        "occasions": LONDON_OCCASIONS,
        "selected_occasion": selected_occasion,
        "intensities": INTENSITIES,
        "selected_intensity": selected_intensity,
        "sort": sort,
        "view_mode": view_mode,
        "suggestions": suggestions,
        "retailers": LONDON_RETAILERS[:3],
    })


def detail(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    meta = _perfume_meta(perfume)
    similar = Perfume.objects.filter(Q(scent_1__in=meta["notes"]) | Q(scent_2__in=meta["notes"]) | Q(scent_3__in=meta["notes"])).exclude(pk=pk).distinct()[:6]
    fav_ids = request.session.get("favourites", [])
    return render(request, "perfumes/detail.html", {"p": perfume, "meta": meta, "similar": similar, "retailers": LONDON_RETAILERS, "is_favourite": perfume.id in fav_ids})


def toggle_favourite(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    favs = request.session.get("favourites", [])
    if perfume.id in favs:
        favs.remove(perfume.id)
        messages.info(request, f"Removed {perfume.name} from favourites.")
    else:
        favs.append(perfume.id)
        messages.success(request, f"Added {perfume.name} to favourites.")
    request.session["favourites"] = favs
    return redirect(request.META.get("HTTP_REFERER") or reverse("perfume_detail", args=[pk]))


def favourites(request):
    favs = request.session.get("favourites", [])
    perfumes = Perfume.objects.filter(id__in=favs)
    return render(request, "perfumes/favourites.html", {"perfumes": perfumes})


def compare(request):
    ids = request.GET.getlist("ids") or request.GET.get("ids", "").split(",")
    ids = [i for i in ids if str(i).isdigit()][:4]
    selected = list(Perfume.objects.filter(id__in=ids)) if ids else []
    all_perfumes = Perfume.objects.all().order_by("brand", "name")[:160]
    comparison = [{"perfume": p, "meta": _perfume_meta(p)} for p in selected]
    return render(request, "perfumes/compare.html", {"comparison": comparison, "all_perfumes": all_perfumes})


def brands(request):
    brand_rows = Perfume.objects.values("brand").annotate(total=Count("id"), avg_price=Avg("price")).exclude(brand="").order_by("brand")
    return render(request, "perfumes/brands.html", {"brands": brand_rows})


def notes(request):
    note_cards = []
    for value, label in SCENT_CHOICES:
        count = Perfume.objects.filter(Q(scent_1=value) | Q(scent_2=value) | Q(scent_3=value)).count()
        if count:
            note_cards.append({"value": value, "label": label, "count": count})
    return render(request, "perfumes/notes.html", {"notes": note_cards})


@staff_member_required
def luxe_admin(request):
    top_notes = []
    for value, label in SCENT_CHOICES:
        count = Perfume.objects.filter(Q(scent_1=value) | Q(scent_2=value) | Q(scent_3=value)).count()
        if count:
            top_notes.append({"label": label, "count": count})
    top_notes = sorted(top_notes, key=lambda x: x["count"], reverse=True)[:8]
    context = {
        "total_users": User.objects.count(),
        "total_perfumes": Perfume.objects.count(),
        "total_brands": Perfume.objects.exclude(brand="").values("brand").distinct().count(),
        "total_searches": request.session.get("search_count", 0),
        "submissions": SurveySubmission.objects.count(),
        "top_perfumes": Perfume.objects.order_by("-price")[:8],
        "top_notes": top_notes,
        "recent_submissions": SurveySubmission.objects.select_related("user", "result_mood").order_by("-created_at")[:8],
        "questions": SurveyQuestion.objects.count(),
    }
    return render(request, "admin_panel/dashboard.html", context)
