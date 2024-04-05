from django.urls import path, re_path

from .views import StartView, wizard_view

form_name = "transactional-licence-form-steps"
form_view = wizard_view("%s-step" % form_name)

urlpatterns = [
    path("", StartView.as_view(), name="transactional-licence-form"),
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
