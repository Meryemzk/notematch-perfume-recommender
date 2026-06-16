from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users.views import login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("survey/", include("survey.urls")),
    path("perfumes/", include("perfumes.urls")),
    path("users/", include("users.urls")),
]
