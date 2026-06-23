from django.contrib import admin
from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer


class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 0


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text")
    ordering = ("order",)
    inlines = [SurveyOptionInline]


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "result_mood", "price_range", "total_energic", "total_relax")
    list_filter = ("result_mood", "price_range", "created_at")
    readonly_fields = ("created_at",)


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "option")
