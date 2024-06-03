from django.urls import re_path

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
    re_path(
        "^/?$",
        StartView1.as_view(),
        name="transactional-licence-form",
    ),
    re_path(
        "^/licence-application-process/?$",
        StartView2.as_view(),
        name="transactional-licence-form-page-2",
    ),
    re_path(
        "^/what-you-need-to-apply-for-a-licence/?$",
        StartView3.as_view(),
        name="transactional-licence-form-page-3",
    ),
    re_path(
        "^/download-application/?$",
        DownloadView.as_view(),
        name="application-download-page",
    ),
    re_path(
        "^/confirmation/?$",
        ConfirmationView.as_view(),
        name="transactional-licence-form-confirmation",
    ),
    re_path(
        r"^/steps/(?P<step>.+)/?$",
        form_view,
        name="%s-step" % form_name,
    ),
    re_path(
        "^/steps/?$",
        form_view,
        name=form_name,
    ),
]
