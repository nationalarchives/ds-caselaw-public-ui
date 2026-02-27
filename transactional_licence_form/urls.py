from django.http import HttpResponseRedirect
from django.urls import re_path, reverse

from .views import (
    ConfirmationView,
    wizard_view,
)

form_name = "transactional-licence-form-steps"
form_view = wizard_view("%s-step" % form_name)

urlpatterns = [
    re_path(
        "^/?$",
        lambda request: HttpResponseRedirect(reverse("what_you_can_do_freely")),
        name="transactional-licence-form",
    ),
    re_path(
        "^/licence-application-process/?$",
        lambda request: HttpResponseRedirect(reverse("licence_application_process")),
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
