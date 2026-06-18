from django.contrib import admin
from .models import Mood, SurveyQuestion, SurveyOption, SurveySubmission, SurveyAnswer, UserPreferenceProfile


class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 3


@admin.action(description="Activate selected survey questions")
def activate_questions(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected survey questions")
def deactivate_questions(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text", "is_active")
    list_editable = ("is_active",)
    ordering = ("order",)
    search_fields = ("text",)
    actions = [activate_questions, deactivate_questions]
    inlines = [SurveyOptionInline]


@admin.register(UserPreferenceProfile)
class UserPreferenceProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3", "preferred_gender", "style_preference", "budget_range", "updated_at")
    list_filter = ("preferred_gender", "style_preference", "budget_range")
    search_fields = ("user__username", "user__first_name", "user__last_name", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3")
    readonly_fields = ("updated_at",)


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "result_mood", "preferred_gender", "style_preference", "budget_range")
    list_filter = ("result_mood", "preferred_gender", "style_preference", "budget_range")
    search_fields = ("user__username", "favourite_perfume_1", "favourite_perfume_2", "favourite_perfume_3")
    readonly_fields = ("created_at",)


admin.site.register(Mood)
admin.site.register(SurveyAnswer)
