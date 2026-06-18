from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("me/", views.profile, name="profile"),
    path("preferences/", views.edit_preferences, name="edit_preferences"),
]
