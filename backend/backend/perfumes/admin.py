from django.contrib import admin
from .models import Perfume


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price", "scent_1", "scent_2", "scent_3")
    list_filter = ("brand", "moods", "scent_1", "scent_2", "scent_3")
    search_fields = ("name", "brand", "notes")
    filter_horizontal = ("moods",)
    fieldsets = (
        ("Perfume information", {"fields": ("name", "brand", "price")}),
        ("Mood and scent matching", {"fields": ("moods", "scent_1", "scent_2", "scent_3")}),
        ("Extra details", {"fields": ("notes",)}),
    )
