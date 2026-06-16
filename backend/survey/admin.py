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

admin.site.register(Mood)
admin.site.register(SurveySubmission)
admin.site.register(SurveyAnswer)
