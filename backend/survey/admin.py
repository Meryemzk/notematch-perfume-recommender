from django.contrib import admin
from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer


class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 1
    fields = ("text", "energic_points", "relax_points", "note_tag")


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text")
    ordering = ("order",)
    search_fields = ("text",)
    inlines = [SurveyOptionInline]


@admin.register(SurveyOption)
class SurveyOptionAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "energic_points", "relax_points", "note_tag")
    list_filter = ("note_tag",)
    search_fields = ("text", "note_tag")


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "result_mood", "total_energic", "total_relax", "top_note_tags")
    list_filter = ("result_mood", "created_at")
    search_fields = ("user__username", "top_note_tags")


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "option")
    list_filter = ("question",)
