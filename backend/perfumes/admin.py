from django.contrib import admin
from .models import Perfume


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = (
        "name", "brand", "gender_category", "price", "rating", "suitable_season",
        "occasion", "availability_status", "retailer",
    )
    list_display_links = ("name",)
    list_editable = ("gender_category", "price", "rating", "availability_status")
    list_filter = (
        "gender_category", "brand", "suitable_season", "occasion", "availability_status",
        "scent_1", "scent_2", "scent_3", "moods",
    )
    search_fields = ("name", "brand", "description", "notes", "retailer")
    filter_horizontal = ("moods",)
    save_on_top = True
    list_per_page = 25
    fieldsets = (
        ("Product identity", {
            "fields": (
                "name", "brand", "image_url", "description", "price", "gender_category",
                "country_of_origin", "year_released", "availability_status", "purchase_link", "retailer",
            )
        }),
        ("Recommendation category", {
            "description": "Use Feminine for W/lady perfumes, Masculine for M/men perfumes, and Unisex only for mixed perfumes. The survey filters strictly from this field.",
            "fields": ("suitable_season", "occasion", "moods"),
        }),
        ("Fragrance notes", {"fields": ("scent_1", "scent_2", "scent_3", "notes")}),
        ("Performance scores", {"fields": ("longevity", "projection", "sillage", "rating")}),
    )


admin.site.site_header = "NoteMatch Professional Admin"
admin.site.site_title = "NoteMatch Admin"
admin.site.index_title = "Analytics, catalogue, survey and recommendation management"
