from django.contrib import admin
from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer


class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 0
    fields = ("text", "energic_points", "relax_points", "note_tag")


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text", "option_count")
    ordering = ("order",)
    search_fields = ("text",)
    inlines = [SurveyOptionInline]

    def option_count(self, obj):
        return obj.options.count()


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "selected_gender_style", "result_mood", "price_range", "total_energic", "total_relax")
    list_filter = ("selected_gender_style", "result_mood", "price_range", "created_at")
    search_fields = ("user__username", "user__email", "top_note_tags")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "option")
    list_filter = ("question", "option")
    search_fields = ("question__text", "option__text")
