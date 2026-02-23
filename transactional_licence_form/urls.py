from django.http import HttpResponseRedirect
from django.urls import re_path, reverse

from .views import (
    ConfirmationView,
    StartView1,
    StartView2,
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
        lambda request: HttpResponseRedirect(reverse("what_you_need_to_apply_for_a_licence")),
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
    re_path(
        "^/home/steps/?$",
        form_view,
        name=form_name,
    ),
]
