from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
    path("search", views.search, name="search"),
    path("results", views.results, name="results"),
    path("", views.index, name="index"),
]
