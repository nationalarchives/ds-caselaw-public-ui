from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)/data.xml", views.detail_xml, name="detail"),
    re_path("(?P<judgment_uri>.*/.*/.*)/data.html", views.detail, name="detail"),
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
    path("judgments/search", views.search, name="search"),
    path("judgments/results", views.results, name="results"),
    path("judgments/", views.index, name="index"),
]
