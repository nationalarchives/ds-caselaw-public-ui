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
from ds_caselaw_utils import courts

from judgments.utils import api_client


class SitemapIndexView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/index.xml"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This is a list of the names of URLs for other (non-dynamic) sitemaps to appear in the index
        map_url_names = ["sitemap_static"]

        # Build full URLs for all of the above, and put them in the context variable
        context["maps"] = [self.request.build_absolute_uri(reverse(map)) for map in map_url_names]

        # Dynamically append a sitemap for each court
        for court in courts.get_listable_courts():
            for year in range(court.start_year, court.end_year):
                context["maps"].append(
                    self.request.build_absolute_uri(
                        reverse("sitemap_court", kwargs={"code": court.canonical_param, "year": year})
                    )
                )

        return context


class SitemapStaticView(TemplateView, TemplateResponseMixin):
    content_type = "application/xml"
    template_name = "sitemaps/sitemap.xml"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This is a list of the names of URLs to reverse and include in the map
        url_names = [
            "home",
            "about_this_service",
            "what_to_expect",
            "how_to_use_this_service",
            "courts_and_tribunals",
            "computational_licence_form",
            "privacy_notice",
            "accessibility_statement",
            "open_justice_licence",
            "terms_of_use",
            "publishing_policy",
            "terms_and_policies",
            "contact_us",
            "courts_and_tribunals_in_fcl",
            "help_and_guidance",
            "how_to_search_find_case_law",
            "understanding_judgments_and_decisions",
            "the_find_case_law_api",
        ]

        context["urls"] = [self.request.build_absolute_uri(reverse(url)) for url in url_names]
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

            context["urls"] = [self.request.build_absolute_uri(result.uri) for result in search_response.results]

        except MarklogicResourceNotFoundError:
            raise Http404()

        return context
