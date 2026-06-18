from django.contrib import admin
from .models import Perfume


@admin.action(description="Mark selected perfumes as active")
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Mark selected perfumes as inactive")
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Mark selected perfumes as featured")
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Set selected perfumes as classic")
def set_classic(modeladmin, request, queryset):
    queryset.update(style_category="classic")


@admin.action(description="Set selected perfumes as new / modern")
def set_new(modeladmin, request, queryset):
    queryset.update(style_category="new")


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "gender_category", "style_category", "price", "is_featured", "is_active")
    list_filter = ("gender_category", "style_category", "moods", "is_featured", "is_active")
    search_fields = ("name", "brand", "notes", "description")
    filter_horizontal = ("moods",)
    list_editable = ("price", "is_featured", "is_active")
    actions = [mark_active, mark_inactive, mark_featured, set_classic, set_new]
    fieldsets = (
        ("Perfume details", {"fields": ("name", "brand", "description", "notes", "moods")}),
        ("Recommendation data", {"fields": ("gender_category", "style_category", "price", "price_source")}),
        ("Admin controls", {"fields": ("is_featured", "is_active")}),
    )
