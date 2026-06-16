from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="perfume_catalog"),
]
