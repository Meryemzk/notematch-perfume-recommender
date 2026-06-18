from django.contrib import admin
from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer


class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 3


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text")
    ordering = ("order",)
    inlines = [SurveyOptionInline]


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "created_at", "result_mood", "preferred_gender",
        "style_preference", "budget_range",
    )
    list_filter = ("result_mood", "preferred_gender", "style_preference", "budget_range")
    search_fields = (
        "user__username", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3",
    )
    readonly_fields = ("created_at",)


admin.site.register(Mood)
admin.site.register(SurveyAnswer)
