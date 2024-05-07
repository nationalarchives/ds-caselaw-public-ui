from django.urls import path, re_path

from .views import (
    ConfirmationView,
    DownloadView,
    StartView1,
    StartView2,
    StartView3,
    wizard_view,
)

form_name = "transactional-licence-form-steps"
form_view = wizard_view("%s-step" % form_name)

urlpatterns = [
    path("", StartView1.as_view(), name="transactional-licence-form"),
    path("/page-2", StartView2.as_view(), name="transactional-licence-form-page-2"),
    path("/page-3", StartView3.as_view(), name="transactional-licence-form-page-3"),
    path(
        "/download-application",
        DownloadView.as_view(),
        name="application-download-page",
    ),
    path(
        "/confirmation",
        ConfirmationView.as_view(),
        name="transactional-licence-form-confirmation",
    ),
    re_path(
        r"^/steps/(?P<step>.+)/$",
        form_view,
        name="%s-step" % form_name,
    ),
    path(
        "/steps",
        form_view,
        name=form_name,
    ),
]
