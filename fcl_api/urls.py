from django.urls import path

from . import views

urlpatterns = [
    path(
        "/bodies",
        views.BodiesView.as_view(),
    ),
]
