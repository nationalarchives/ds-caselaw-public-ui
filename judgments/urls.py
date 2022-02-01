from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),
]
