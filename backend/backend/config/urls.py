from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("", include("core.urls")),
    path("survey/", include("survey.urls")),
    path("perfumes/", include("perfumes.urls")),
    path("users/", include("users.urls")),
]
