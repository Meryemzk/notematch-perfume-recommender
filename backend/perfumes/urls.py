from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="perfume_catalog"),
    path("brands/", views.brands, name="brands"),
    path("notes/", views.notes, name="notes"),
    path("favourites/", views.favourites, name="favourites"),
    path("compare/", views.compare, name="compare"),
    path("admin-panel/", views.luxe_admin, name="luxe_admin"),
    path("<int:pk>/", views.detail, name="perfume_detail"),
    path("<int:pk>/favourite/", views.toggle_favourite, name="toggle_favourite"),
]
