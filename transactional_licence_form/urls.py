from django.urls import path

from .views import FormView

urlpatterns = [path("", FormView.as_view(), name="transactional-licence-form")]
