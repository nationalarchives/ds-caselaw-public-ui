from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path(
        "check-answers",
        views.CheckAnswersView.as_view(),
        name="check_answers",
    ),
    path(
        "any-comments",
        views.AnyCommentsView.as_view(),
        name="any_comments",
    ),
    path(
        "accurate-data-representation",
        views.AccurateDataRepresentationView.as_view(),
        name="accurate_data_representation",
    ),
    path(
        "algorithmic-transparency",
        views.AlgorithmicTransparencyView.as_view(),
        name="algorithmic_transparency",
    ),
    path(
        "discoverability",
        views.DiscoverabilityView.as_view(),
        name="discoverability",
    ),
    path(
        "personal-privacy",
        views.PersonalPrivacyView.as_view(),
        name="personal_privacy",
    ),
    path(
        "anti-bias",
        views.AntiBiasView.as_view(),
        name="anti_bias",
    ),
    path(
        "anti-discriminatory-harm",
        views.AntiDiscriminatoryHarmView.as_view(),
        name="anti_discriminatory_harm",
    ),
    path(
        "appropriate-scrutiny",
        views.AppropriateScrutinyView.as_view(),
        name="appropriate_scrutiny",
    ),
    path(
        "independence-of-the-court",
        views.IndependenceCourtView.as_view(),
        name="independence_of_the_court",
    ),
    path(
        "dignity-of-the-courts",
        views.DignityCourtsView.as_view(),
        name="dignity_of_the_courts",
    ),
    path(
        "statements-and-principles",
        views.StatementsPrinciplestView.as_view(),
        name="statements_and_principles",
    ),
    path(
        "public-statement",
        views.PublicStatementView.as_view(),
        name="public_statement",
    ),
    path(
        "purpose-and-activities",
        views.PurposeActivitiesView.as_view(),
        name="purpose_and_activities",
    ),
    path(
        "your-organisation",
        views.YourOrganisationView.as_view(),
        name="your_organisation",
    ),
    path(
        "submit-details",
        views.SubmitDetailsView.as_view(),
        name="submit_details",
    ),
    path(
        "computational-licence-application",
        views.ComputationalLicenceSubmitView.as_view(),
        name="computational_licence_application",
    ),
    path(
        "computational-licence-form",
        views.ComputationalLicenceFormView.as_view(),
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
