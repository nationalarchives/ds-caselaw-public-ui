from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:judgement_uri>/", views.detail, name="detail"),
]
