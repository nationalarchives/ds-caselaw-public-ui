from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
    re_path("(?P<page>\\d)", views.index, name="index"),
    path("search", views.search, name="search"),
    path("results", views.results, name="results"),
    path("", views.index, name="index"),
]
