from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, register_converter
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from .views.style_guide import StyleGuideView
from .views.errors import NotFoundView, ServerErrorView, PermissionDeniedView
from .views.courts import CourtsTribunalsListView, CourtOrTribunalView
from .views.about import AboutThisServiceView
from .views.accessibility_statement import AccessibilityStatementView
from .views.open_justice_license import OpenJusticeLicenceView
from .views.terms_of_use import TermsOfUseView
from .views.publishing_policy import PublishingPolicyView
from .views.structured_search import StructuredSearchView
from .views.terms_and_policies import TermsAndPoliciesView
from .views.contact_us import ContactUsView
from .views.courts_and_tribunals_in_fcl import CourtsAndTribunalsInFclView
from .views.help_and_guidance import HelpAndGuidanceView
from .views.how_to_search_find_case_law import HowToSearchFindCaseLawView
from .views.understanding_judgements_and_decisions import UnderstandingJudgmentsAndDecisionsView
from .views.the_find_case_law_api import TheFindCaseLawApiView


from .views.check import status
from .views.how_to import HowToUseThisService
from .views.privacy_notice import PrivacyNotice
from .views.schema import schema
from .converters import SchemaFileConverter

register_converter(SchemaFileConverter, "schemafile")

handler404 = NotFoundView.as_view()
handler500 = ServerErrorView.as_view()
handler403 = PermissionDeniedView.as_view()

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path(
        "courts-and-tribunals/<path:param>",
        CourtOrTribunalView.as_view(),
        name="court_or_tribunal",
    ),
    path(
        "courts-and-tribunals",
        CourtsTribunalsListView.as_view(),
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
        AboutThisServiceView.as_view(),
        name="about_this_service",
    ),
    path(
        "how-to-use-this-service",
        HowToUseThisService.as_view(),
        name="how_to_use_this_service",
    ),
    path(
        "privacy-notice",
        PrivacyNotice.as_view(),
        name="privacy_notice",
    ),
    path(
        "accessibility-statement",
        AccessibilityStatementView.as_view(),
        name="accessibility_statement",
    ),
    path(
        "style-guide",
        StyleGuideView.as_view(),
        name="style_guide",
    ),
    path(
        "test-page-please-ignore",
        TemplateView.as_view(template_name="pages/test_page.html", content_type="text/html"),
        name="test_page",
    ),
    path(
        "open-justice-licence",
        OpenJusticeLicenceView.as_view(),
        name="open_justice_licence",
    ),
    path(
        "terms-of-use",
        TermsOfUseView.as_view(),
        name="terms_of_use",
    ),
    path(
        "publishing-policy",
        PublishingPolicyView.as_view(),
        name="publishing_policy",
    ),
    path(
        "structured_search",
        StructuredSearchView.as_view(),
        name="structured_search",
    ),
    path(
        "terms-and-policies",
        TermsAndPoliciesView.as_view(),
        name="terms_and_policies",
    ),
    path(
        "contact-us",
        ContactUsView.as_view(),
        name="contact_us",
    ),
    path(
        "courts-and-tribunals-in-fcl",
        CourtsAndTribunalsInFclView.as_view(),
        name="courts_and_tribunals_in_fcl",
    ),
    path(
        "help-and-guidance",
        HelpAndGuidanceView.as_view(),
        name="help_and_guidance",
    ),
    path(
        "how-to-search-find-case-law",
        HowToSearchFindCaseLawView.as_view(),
        name="how_to_search_find_case_law",
    ),
    path(
        "understanding-judgments-and-decisions",
        UnderstandingJudgmentsAndDecisionsView.as_view(),
        name="understanding_judgments_and_decisions",
    ),
    path(
        "the-find-case-law-api",
        TheFindCaseLawApiView.as_view(),
        name="the_find_case_law_api",
    ),
    path(
        "check",
        status,
        name="check",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "googleb0ce3f99fae65e7c.html",
        TemplateView.as_view(template_name="googleb0ce3f99fae65e7c.html", content_type="text/html"),
    ),
    path(
        "schema/<schemafile:schemafile>",
        cache_page(60 * 60)(schema),
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
            PermissionDeniedView.as_view(),
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            NotFoundView.as_view(),
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", ServerErrorView.as_view()),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
