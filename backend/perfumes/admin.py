from django.contrib import admin
from .models import Perfume


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "gender_category", "style_category", "price")
    list_filter = ("gender_category", "style_category", "moods")
    search_fields = ("name", "brand", "notes")
    filter_horizontal = ("moods",)
