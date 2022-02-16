from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("(?P<judgment_uri>.*/.*/.*)", views.edit, name="edit"),
    path("update", views.update, name="update"),
]
