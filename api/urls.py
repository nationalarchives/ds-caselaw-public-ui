from rest_framework import routers

from .viewsets import bodies

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"bodies", bodies.BodiesViewSet, basename="body")

urlpatterns = router.urls
