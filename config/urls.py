from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponseRedirect
from django.urls import include, path, register_converter, reverse
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView, TemplateView

from judgments.views.advanced_search import StructuredSearchView, advanced_search

from .converters import SchemaFileConverter
from .views import static as static_views
from .views.check import status
from .views.courts import CourtOrTribunalView, CourtsTribunalsListView
from .views.errors import NotFoundView, PermissionDeniedView, ServerErrorView
from .views.schema import schema
from .views.sitemaps import SitemapCourtsView, SitemapCourtView, SitemapIndexView, SitemapStaticView
from .views.style_guide import StyleGuideView

register_converter(SchemaFileConverter, "schemafile")

handler404 = NotFoundView.as_view()
handler500 = ServerErrorView.as_view()
handler403 = PermissionDeniedView.as_view()


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Pages for viewing court details
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
    # Search
    path(
        "search",
        advanced_search,
        name="search",
    ),
    path(
        "search/advanced",
        StructuredSearchView.as_view(),
        name="advanced_search",
    ),
    path(
        "judgments/results",
        lambda request: HttpResponseRedirect(reverse("search") + "?" + request.GET.urlencode()),
    ),
    path(
        "judgments/search",
        lambda request: HttpResponseRedirect(reverse("search") + "?" + request.GET.urlencode()),
    ),
    path(
        "judgments/advanced_search",
        lambda request: HttpResponseRedirect(reverse("advanced_search") + "?" + request.GET.urlencode()),
    ),
    path(
        "advanced_search",
        lambda request: HttpResponseRedirect(reverse("advanced_search") + "?" + request.GET.urlencode()),
    ),
    path(
        "structured_search",
        lambda request: HttpResponseRedirect(reverse("advanced_search") + "?" + request.GET.urlencode()),
    ),
    # Static pages
    path(
        "about-this-service",
        static_views.AboutThisServiceView.as_view(),
        name="about_this_service",
    ),
    path(
        "accessibility-statement",
        static_views.AccessibilityStatementView.as_view(),
        name="accessibility_statement",
    ),
    path(
        "contact-us",
        static_views.ContactUsView.as_view(),
        name="contact_us",
    ),
    path(
        "courts-and-tribunals-in-fcl",
        static_views.CourtsAndTribunalsInFclView.as_view(),
        name="courts_and_tribunals_in_fcl",
    ),
    path(
        "help-and-guidance",
        static_views.HelpAndGuidanceView.as_view(),
        name="help_and_guidance",
    ),
    path(
        "how-to-search-find-case-law",
        static_views.HowToSearchFindCaseLawView.as_view(),
        name="how_to_search_find_case_law",
    ),
    path(
        "how-to-use-this-service",
        static_views.HowToUseThisService.as_view(),
        name="how_to_use_this_service",
    ),
    path(
        "open-justice-licence",
        static_views.OpenJusticeLicenceView.as_view(),
        name="open_justice_licence",
    ),
    path(
        "privacy-notice",
        static_views.PrivacyNotice.as_view(),
        name="privacy_notice",
    ),
    path(
        "publishing-policy",
        static_views.PublishingPolicyView.as_view(),
        name="publishing_policy",
    ),
    path(
        "terms-and-policies",
        static_views.TermsAndPoliciesView.as_view(),
        name="terms_and_policies",
    ),
    path(
        "terms-of-use",
        static_views.TermsOfUseView.as_view(),
        name="terms_of_use",
    ),
    path(
        "the-find-case-law-api",
        lambda request: HttpResponseRedirect("https://nationalarchives.github.io/ds-find-caselaw-docs/public"),
        name="the_find_case_law_api",
    ),
    path(
        "understanding-judgments-and-decisions",
        static_views.UnderstandingJudgmentsAndDecisionsView.as_view(),
        name="understanding_judgments_and_decisions",
    ),
    path(
        "what-to-expect",
        lambda request: HttpResponseRedirect(reverse("about_this_service")),
        name="what_to_expect",
    ),
    # Styleguide
    path(
        "style-guide",
        StyleGuideView.as_view(),
        name="style_guide",
    ),
    # Test page
    path(
        "test-page-please-ignore",
        TemplateView.as_view(template_name="pages/test_page.html", content_type="text/html"),
        name="test_page",
    ),
    # Sitemap
    path(
        "sitemap.xml",
        SitemapIndexView.as_view(),
        name="sitemap_index",
    ),
    path(
        "sitemap-static.xml",
        SitemapStaticView.as_view(),
        name="sitemap_static",
    ),
    path(
        "sitemap-courts.xml",
        SitemapCourtsView.as_view(),
        name="sitemap_courts",
    ),
    path(
        "sitemap-court-<path:code>-<int:year>.xml",
        SitemapCourtView.as_view(),
        name="sitemap_court",
    ),
    # Site status
    path(
        "check",
        status,
        name="check",
    ),
    # Files for non-humans
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "trust.txt",
        TemplateView.as_view(template_name="trust.txt", content_type="text/plain"),
    ),
    path(
        ".well-known/trust.txt",
        RedirectView.as_view(url="/trust.txt"),
    ),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("images/favicons/favicon.ico"))),
    path(
        "googleb0ce3f99fae65e7c.html",
        TemplateView.as_view(template_name="googleb0ce3f99fae65e7c.html", content_type="text/html"),
    ),
    path(
        "schema/<schemafile:schemafile>",
        cache_page(60 * 60)(schema),
        name="schema",
    ),
    # License application
    path(
        "computational-licence-form",
        lambda request: HttpResponseRedirect("/re-use-find-case-law-records"),
        name="computational_licence_form",
    ),
    path("re-use-find-case-law-records", include("transactional_licence_form.urls")),
    # Judgment resolution
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
