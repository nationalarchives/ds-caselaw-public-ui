from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic.base import TemplateView

from . import views


def redirect(request, uri):
    return HttpResponseRedirect(f"/{uri.lower()}")


urlpatterns = [
    re_path("^(?P<uri>.*[A-Z].*?)/?$", redirect),
    re_path("^(?P<uri>.*)/$", redirect),
    path(
        "transactional-licence-form",
        views.TransactionalLicenceFormView.as_view(),
        name="transactional_licence_form",
    ),
    path(
        "what-to-expect",
        views.WhatToExpectView.as_view(),
        name="what_to_expect",
    ),
    path(
        "how-to-use-this-service",
        views.HowToUseThisService.as_view(),
        name="how_to_use_this_service",
    ),
    path(
        "accessibility-statement",
        views.AccessibilityStatement.as_view(),
        name="accessibility_statement",
    ),
    path(
        "open-justice-licence",
        views.OpenJusticeLicenceView.as_view(),
        name="open_justice_licence",
    ),
    path(
        "terms-of-use",
        views.TermsOfUseView.as_view(),
        name="terms_of_use",
    ),
    path(
        "structured_search",
        views.StructuredSearchView.as_view(),
        name="structured_search",
    ),
    path(
        "no_results",
        views.NoResultsView.as_view(),
        name="no_results",
    ),
    path(
        "check",
        views.CheckView.as_view(),
        name="check",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("", include("judgments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
