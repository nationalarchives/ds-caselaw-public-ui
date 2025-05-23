from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from rest_framework import routers

from .viewsets import bodies, identifier_types

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"bodies", bodies.BodiesViewSet, basename="body")
router.register(r"identifier-types", identifier_types.IdentifierTypesViewSet, basename="identifier_type")

urlpatterns = router.urls + [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
