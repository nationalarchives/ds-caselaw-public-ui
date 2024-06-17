from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, register_converter
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from . import views
from .converters import SchemaFileConverter

register_converter(SchemaFileConverter, "schemafile")

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path(
        "courts-and-tribunals/<path:param>",
        views.CourtOrTribunalView.as_view(),
        name="court_or_tribunal",
    ),
    path(
        "courts-and-tribunals",
        views.CourtsTribunalsListView.as_view(),
        name="courts_and_tribunals",
    ),
    path(
        "computational-licence-form",
        lambda request: HttpResponseRedirect("/re-use-find-case-law-records"),
        name="computational_licence_form",
    ),
    path(
        "what-to-expect",
        lambda request: HttpResponseRedirect("/about-this-service"),
        name="what_to_expect",
    ),
    path(
        "about-this-service",
        views.AboutThisServiceView.as_view(),
        name="about_this_service",
    ),
    path(
        "how-to-use-this-service",
        views.HowToUseThisService.as_view(),
        name="how_to_use_this_service",
    ),
    path(
        "privacy-notice",
        views.PrivacyNotice.as_view(),
        name="privacy_notice",
    ),
    path(
        "accessibility-statement",
        views.AccessibilityStatement.as_view(),
        name="accessibility_statement",
    ),
    path(
        "style-guide",
        views.StyleGuide.as_view(),
        name="style_guide",
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
        "publishing-policy",
        views.PublishingPolicyView.as_view(),
        name="publishing_policy",
    ),
    path(
        "structured_search",
        views.StructuredSearchView.as_view(),
        name="structured_search",
    ),
    path(
        "check",
        views.CheckView.as_view(),
        name="check",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "googleb0ce3f99fae65e7c.html",
        TemplateView.as_view(
            template_name="googleb0ce3f99fae65e7c.html", content_type="text/html"
        ),
    ),
    path(
        "schema/<schemafile:schemafile>",
        cache_page(60 * 60)(views.schema),
        name="schema",
    ),
    path("re-use-find-case-law-records", include("transactional_licence_form.urls")),
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
