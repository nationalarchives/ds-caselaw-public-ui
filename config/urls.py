from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path, register_converter, reverse
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView, TemplateView

from config.views.storybook import storybook_render_view
from judgments import views as content_views
from judgments.views import about_this_service as about_this_service_views
from judgments.views import help_and_support as help_and_support_views
from judgments.views import permissions_and_licensing as permissions_and_licensing_views
from judgments.views import search_and_browse as search_and_browse_views
from judgments.views import understanding_case_law as understanding_case_law_views
from judgments.views.search import (
    AdvancedSearchView,
    SearchResultsView,
)

from .converters import SchemaFileConverter

# from .views import static as static_views
from .views.check import status
from .views.components import ComponentsView
from .views.courts import (
    CourtOrTribunalView,
    CourtsTribunalsListView,
)
from .views.errors import NotFoundView, PermissionDeniedView, ServerErrorView
from .views.glossary import GlossaryView
from .views.schema import schema
from .views.sitemaps import SitemapCourtsView, SitemapCourtView, SitemapIndexView, SitemapStaticView

register_converter(SchemaFileConverter, "schemafile")

handler404 = NotFoundView.as_view()
handler500 = ServerErrorView.as_view()
handler403 = PermissionDeniedView.as_view()


non_public_urls = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "storybook-render",
        storybook_render_view,
        name="storybook_render",
    ),
    path(
        "test-page-please-ignore",
        TemplateView.as_view(template_name="pages/test_page.html", content_type="text/html"),
        name="test_page",
    ),
    path(
        "components",
        ComponentsView.as_view(),
        name="components",
    ),
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
    re_path("schema/.*", NotFoundView.as_view(), kwargs={"exception": Exception("Schema not found")}),
]

root_content_urls = [
    path(
        "about-this-service",
        about_this_service_views.AboutThisServiceView.as_view(),
        name="about_this_service",
    ),
    path(
        "help-and-support",
        help_and_support_views.HelpAndSupportView.as_view(),
        name="help_and_support",
    ),
    path(
        "understanding-case-law",
        understanding_case_law_views.UnderstandingCaseLawView.as_view(),
        name="understanding_case_law",
    ),
    path(
        "permissions-and-licensing",
        permissions_and_licensing_views.PermissionsAndLicensingView.as_view(),
        name="permissions_and_licensing",
    ),
    path(
        "search-and-browse",
        search_and_browse_views.SearchAndBrowseView.as_view(),
        name="search_and_browse",
    ),
    path(
        "accessibility-statement",
        content_views.AccessibilityStatementView.as_view(),
        name="accessibility_statement",
    ),
    path(
        "privacy-notice",
        content_views.PrivacyNoticeView.as_view(),
        name="privacy_notice",
    ),
    path(
        "terms-and-policies",
        lambda request: HttpResponseRedirect(reverse("terms_of_use")),
        name="terms_and_policies",
    ),
    path(
        "terms-of-use",
        content_views.TermsOfUseView.as_view(),
        name="terms_of_use",
    ),
    path(
        "the-find-case-law-api",
        lambda request: HttpResponseRedirect("https://nationalarchives.github.io/ds-find-caselaw-docs/public"),
        name="the_find_case_law_api",
    ),
    path(
        "what-to-expect",
        lambda request: HttpResponseRedirect(reverse("about_this_service")),
        name="what_to_expect",
    ),
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
]

about_this_service_urls = [
    path(
        "what-we-provide",
        about_this_service_views.WhatWeProvideView.as_view(),
        name="what_we_provide",
    ),
    path(
        "courts-and-date-coverage",
        about_this_service_views.CourtsAndDateCoverageView.as_view(),
        name="courts_and_date_coverage",
    ),
    path(
        "publishing-policy",
        about_this_service_views.PublishingPolicyView.as_view(),
        name="publishing_policy",
    ),
    path(
        "courts-and-tribunals-in-fcl",
        about_this_service_views.CourtsAndTribunalsInFclView.as_view(),
        name="courts_and_tribunals_in_fcl",
    ),
    path(
        "about-find-case-law",
        about_this_service_views.AboutFindCaseLawView.as_view(),
        name="about_find_case_law",
    ),
]

help_and_support_urls = [
    path(
        "contact-us",
        help_and_support_views.ContactUsView.as_view(),
        name="contact_us",
    ),
    path(
        "help-and-guidance",
        lambda request: HttpResponseRedirect(reverse("help_and_support")),
    ),
    path(
        "user-research",
        help_and_support_views.UserResearchView.as_view(),
        name="user_research",
    ),
    path(
        "search-tips",
        help_and_support_views.SearchTipsView.as_view(),
        name="search_tips",
    ),
    path(
        "feedback",
        help_and_support_views.FeedbackView.as_view(),
        name="feedback",
    ),
    path(
        "glossary",
        GlossaryView.as_view(),
        name="glossary",
    ),
]

understanding_case_law_urls = [
    path(
        "reading-judgments",
        understanding_case_law_views.ReadingJudgmentsView.as_view(),
        name="reading_judgments",
    ),
    path(
        "understanding-judgments-and-decisions",
        understanding_case_law_views.UnderstandingJudgmentsAndDecisionsView.as_view(),
        name="understanding_judgments_and_decisions",
    ),
]

search_and_browse_urls = [
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
        "how-to-search-find-case-law",
        search_and_browse_views.HowToSearchFindCaseLawView.as_view(),
        name="how_to_search_find_case_law",
    ),
    path(
        "how-to-use-this-service",
        lambda request: HttpResponseRedirect(reverse("how_to_search_find_case_law")),
        name="how_to_use_this_service",
    ),
    path(
        "browse-courts-and-tribunals",
        search_and_browse_views.BrowseCourtsAndTribunalsView.as_view(),
        name="browse_courts_and_tribunals",
    ),
]

permissions_and_licensing_urls = [
    path(
        "what-you-can-do-freely",
        permissions_and_licensing_views.WhatYouCanDoFreelyView.as_view(),
        name="what_you_can_do_freely",
    ),
    path(
        "when-you-need-permission",
        permissions_and_licensing_views.WhenYouNeedPermissionView.as_view(),
        name="when_you_need_permission",
    ),
    path(
        "using-find-case-law-records",
        permissions_and_licensing_views.UsingFindCaseLawRecordsView.as_view(),
        name="using_find_case_law_records",
    ),
    path(
        "what-you-need-to-apply-for-a-licence",
        permissions_and_licensing_views.WhatYouNeedToApplyForALicenceView.as_view(),
        name="what_you_need_to_apply_for_a_licence",
    ),
    path(
        "how-to-get-permission",
        permissions_and_licensing_views.HowToGetPermissionView.as_view(),
        name="how_to_get_permission",
    ),
    path(
        "licence-application-process",
        permissions_and_licensing_views.LicenceApplicationProcessView.as_view(),
        name="licence_application_process",
    ),
    path(
        "apply-for-a-licence",
        permissions_and_licensing_views.ApplyForALicenceView.as_view(),
        name="apply_for_a_licence",
    ),
    path(
        "legal-framework",
        permissions_and_licensing_views.LegalFrameworkView.as_view(),
        name="legal_framework",
    ),
    path(
        "open-justice-licence",
        permissions_and_licensing_views.OpenJusticeLicenceView.as_view(),
        name="open_justice_licence",
    ),
    path(
        "computational-licence-form",
        lambda request: HttpResponseRedirect(reverse("transactional-licence-form")),
    ),
    path("re-use-find-case-law-records", include("transactional_licence_form.urls")),
]


search_urls = [
    path(
        "search",
        SearchResultsView.as_view(),
        name="search",
    ),
    path(
        "search/advanced",
        AdvancedSearchView.as_view(),
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
]

judgment_urls = [path("", include("judgments.urls"))]


urlpatterns = (
    root_content_urls
    + about_this_service_urls
    + help_and_support_urls
    + understanding_case_law_urls
    + search_and_browse_urls
    + permissions_and_licensing_urls
    + search_urls
    + non_public_urls
    + judgment_urls
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


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
