import datetime
from typing import Any, List, Optional
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.responses.search_result import SearchResult
from caselawclient.search_parameters import SearchParameters
from django.contrib.syndication.views import Feed
from django.core.exceptions import BadRequest
from django.http import Http404
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .utils import api_client, paginator
from .utils.search_request_to_parameters import search_request_to_parameters


def _add_page_to_url(url: str, page: int = 1) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    query_dict = parse_qs(query)
    print(query_dict, url)
    query_dict["page"] = [
        str(page),
    ]
    new_query = urlencode(query_dict, doseq=True)
    return_value = urlunsplit((scheme, netloc, path, new_query, fragment))
    print(return_value)
    return return_value


class JudgmentAtomFeed(Atom1Feed):
    def root_attributes(self):
        attrs = super().root_attributes()
        attrs["xmlns:tna"] = "https://caselaw.nationalarchives.gov.uk"
        return attrs

    def add_item_elements(self, handler, item) -> None:
        super().add_item_elements(handler, item)
        handler.addQuickElement("tna:uri", item.get("uri", ""))
        handler.addQuickElement("tna:contenthash", item.get("content_hash", ""))

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        pagination = paginator(self.feed["page"], self.feed["total"])
        handler.addQuickElement("link", "", {"rel": "first", "href": _add_page_to_url(self.feed["feed_url"], page=1)})
        handler.addQuickElement(
            "link",
            "",
            {
                "rel": "last",
                "href": _add_page_to_url(self.feed["feed_url"], page=pagination["number_of_pages"]),
            },
        )

        # In atom feeds, next and previous are the opposite to what we would expect
        # Next means to go to the later entries, previous means to go to older entries
        if pagination["has_next_page"]:
            handler.addQuickElement(
                "link",
                "",
                {
                    "rel": "next",
                    "href": _add_page_to_url(self.feed["feed_url"], page=pagination["next_page"]),
                },
            )

        if pagination["has_prev_page"]:
            handler.addQuickElement(
                "link",
                "",
                {
                    "rel": "previous",
                    "href": _add_page_to_url(self.feed["feed_url"], page=pagination["prev_page"]),
                },
            )


class JudgmentsFeed(Feed):
    feed_type = JudgmentAtomFeed
    author_name = "The National Archives"

    def items(self, obj) -> List[SearchResult]:
        return obj["search_response"].results

    def item_description(self, item) -> str:
        return ""

    def item_title(self, item):
        return item.name

    def item_link(self, item) -> str:
        return reverse("detail", kwargs={"document_uri": item.uri})

    def item_author_name(self, item) -> Optional[str]:
        return item.court

    def item_extra_kwargs(self, item):
        extra_kwargs = super().item_extra_kwargs(item)
        extra_kwargs["uri"] = item.uri
        extra_kwargs["content_hash"] = item.content_hash
        return extra_kwargs

    def item_updateddate(self, item: SearchResult) -> datetime.datetime:
        date_string = item.transformation_date or "1970-01-01T00:00:00.000"
        return datetime.datetime.fromisoformat(date_string)

    def item_pubdate(self, item: SearchResult) -> Optional[datetime.datetime]:
        return item.date

    def feed_extra_kwargs(self, obj):
        extra_kwargs = super().item_extra_kwargs(obj)
        extra_kwargs["total"] = int(obj["search_response"].total)
        extra_kwargs["page"] = obj["page"]
        return extra_kwargs


class LatestJudgmentsFeed(JudgmentsFeed):
    def link(self, obj):
        page = obj.get("page", 1)
        return f"/{obj['slug']}/atom.xml?page={page}&order={obj.get('order')}"

    def title(self, obj):
        if not obj["slug"]:
            return "Latest judgments"

        return f'Latest judgments for {obj.get("slug", "/")}'

    def get_object(self, request, court=None, subdivision=None, year=None):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            # e.g. the user provided ?page= or ?page=jam
            raise Http404

        court_query = "/".join(filter(lambda x: x is not None, [court, subdivision]))
        slugs = filter(lambda x: x is not None, [court, subdivision, year])
        slug = "/".join([str(s) for s in slugs])
        order = request.GET.get("order", "-date")

        search_parameters = SearchParameters(
            court=court_query if court_query else None,
            date_from=(datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d") if year else None),
            date_to=(datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d") if year else None),
            order=order,
            page=int(page),
        )
        search_response = search_judgments_and_parse_response(api_client, search_parameters)

        return {
            "slug": slug,
            "search_response": search_response,
            "page": page,
            "order": order,
        }


class SearchJudgmentsFeed(JudgmentsFeed):
    def link(self, obj):
        return obj["self_uri"]

    def title(self, obj):
        if not obj["query_string"]:
            return "Search results"

        return f'Search results for {obj.get("query_string")}'

    def feed_url(self, obj):
        return obj["self_uri"]

    def _base_feed_uri(self, request: HttpRequest) -> str:
        """Remove the page from the URI and make fully qualified"""
        # e.g. /atom.xml?path=3&query=jam
        full_path = request.get_full_path()
        scheme, netloc, path, query, fragment = urlsplit(full_path)
        query_dict = parse_qs(query)
        if "page" in query_dict.keys():
            del query_dict["page"]
        new_query = urlencode(query_dict, doseq=True)
        scheme = "https"
        netloc = "caselaw.nationalarchives.gov.uk"
        return urlunsplit((scheme, netloc, path, new_query, fragment))

    def get_object(self, request: HttpRequest) -> dict[str, Any]:
        # Taken verbatim from judgments/views/advanced_search advanced_search()
        order = request.GET.get("order", default=None)
        if order not in [None, "-date", "date", "-transform", "transform", "updated", "-updated"]:
            raise BadRequest("Sort order should be one of date, transform or updated, or -date, -transform or -updated")

        search_parameters: SearchParameters = search_request_to_parameters(request)
        # set a sensible default, since the order could default to relevance if there's a text search term.
        if order is None:
            search_parameters.order = "-date"

        search_response = search_judgments_and_parse_response(api_client, search_parameters)
        return {
            "query_string": request.GET.get("query", default=""),
            "self_uri": self._base_feed_uri(request),
            "search_response": search_response,
            "page": search_parameters.page,
            "order": search_parameters.order,
        }
