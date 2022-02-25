from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
    path("judgments/search", views.search, name="search"),
    path("judgments/results", views.results, name="results"),
    path("", views.index, name="home"),
]
