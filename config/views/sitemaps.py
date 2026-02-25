import datetime
from typing import Any, Union

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.http import Http404
from django.urls import reverse
from django.views.generic.base import TemplateResponseMixin, TemplateView

from judgments.models.court_dates import CourtDates
from judgments.utils import api_client


class SitemapIndexView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/index.xml"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This is a list of the names of URLs for other sitemaps to appear in the index
        map_url_names = [
            "sitemap_static",
            "sitemap_courts",
        ]

        # Build full URLs for all of the above, and put them in the context variable
        context["maps"] = [self.request.build_absolute_uri(reverse(map)) for map in map_url_names]

        # Dynamically append a sitemap for each court
        for court in CourtDates.objects.all():
            for year in range(court.start_year, court.end_year + 1):
                context["maps"].append(
                    self.request.build_absolute_uri(
                        reverse("sitemap_court", kwargs={"code": court.param, "year": year})
                    )
                )

        return context


class SitemapStaticView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/sitemap.xml"
    # This is a list of the names of URLs to reverse and include in the map
    url_names = [
        "home",
        # Understanding case law
        "understanding_case_law",
        "reading_judgments",
        "understanding_judgments_and_decisions",
        # Search and browse
        "search_and_browse",
        "advanced_search",
        "browse_courts_and_tribunals",
        "courts_and_tribunals",
        # About this service
        "about_this_service",
        "what_we_provide",
        "courts_and_date_coverage",
        "courts_and_tribunals_in_fcl",
        "publishing_policy",
        # Permissions and licencing
        "permissions_and_licencing",
        "open_justice_licence",
        "what_you_can_do_freely",
        "when_you_need_permission",
        "how_to_get_permission",
        "legal_framework",
        # Help and support
        "help_and_support",
        "search_tips",
        "contact_us",
        "feedback",
        # Footer
        "terms_of_use",
        "privacy_notice",
        "accessibility_statement",
        "apply_for_a_licence",
        "user_research",
    ]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["items"] = [{"url": self.request.build_absolute_uri(reverse(url))} for url in self.url_names]
        return context


class SitemapCourtsView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/sitemap.xml"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["items"] = [
            {"url": self.request.build_absolute_uri(reverse("court_or_tribunal", kwargs={"param": court.param}))}
            for court in CourtDates.objects.all()
        ]

        return context


class SitemapCourtView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/sitemap.xml"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        court_query = self.kwargs.get("code")
        year: Union[int, None] = self.kwargs.get("year")

        try:
            search_parameters = SearchParameters(
                court=court_query if court_query else None,
                date_from=(datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d") if year else None),
                date_to=(datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d") if year else None),
                order="-date",
                page=1,
                page_size=50000,
            )
            search_response = search_judgments_and_parse_response(api_client, search_parameters)

            context["items"] = [
                {
                    "url": self.request.build_absolute_uri("/" + result.slug),
                    "lastmod": datetime.datetime.strptime(result.transformation_date, "%Y-%m-%dT%H:%M:%S")
                    .date()
                    .isoformat(),
                }
                for result in search_response.results
            ]

        except MarklogicResourceNotFoundError:
            raise Http404()

        return context
