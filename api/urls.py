from rest_framework import routers

from .viewsets import bodies

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"bodies", bodies.BodiesViewSet, basename="body")
# router.register(r'documents', AccountViewSet)

# urlpatterns = [
#     path(
#         "/bodies",
#         bodies.BodiesView.as_view(),
#     ),
#     path(
#         "/documents",
#         documents.DocumentsView.as_view(),
#     ),
# ]

urlpatterns = router.urls
