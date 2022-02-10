from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<page>", views.index, name="index"),
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
    path("source", views.source, name="source"),
    path("structured_search", views.structured_search, name="structured_search"),
]
