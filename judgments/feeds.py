import datetime

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import SearchResult
from .utils import perform_advanced_search


class JudgmentAtomFeed(Atom1Feed):
    def root_attributes(self):
        attrs = super().root_attributes()
        attrs["xmlns:tna"] = "https://caselaw.nationalarchives.gov.uk"
        return attrs

    def add_item_elements(self, handler, item) -> None:
        super().add_item_elements(handler, item)
        handler.addQuickElement("tna:uri", item.get("uri", ""))


class LatestJudgmentsFeed(Feed):
    feed_type = JudgmentAtomFeed
    author_name = "The National Archives"

    def get_object(self, request, court=None, subdivision=None, year=None):
        return {"court": court, "subdivision": subdivision, "year": year}

    def title(self, obj):
        if not obj["court"] and not obj["subdivision"] and not obj["year"]:
            return "Latest judgments"

        slugs = filter(
            lambda x: x is not None, [obj["court"], obj["subdivision"], obj["year"]]
        )
        return f'Latest judgments for /{"/".join([str(s) for s in slugs])}'

    def link(self, obj):
        slugs = filter(
            lambda x: x is not None, [obj["court"], obj["subdivision"], obj["year"]]
        )
        return "/" + "/".join([str(s) for s in slugs])

    def items(self, obj):
        court = obj["court"]
        subdivision = obj["subdivision"]
        year = obj["year"]

        court_query = "/".join(filter(lambda x: x is not None, [court, subdivision]))
        model = perform_advanced_search(
            court=court_query if court_query else None,
            date_from=datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
            if year
            else None,
            date_to=datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
            if year
            else None,
            order="-date",
        )

        return [SearchResult.create_from_node(result) for result in model.results]

    def item_description(self, item: SearchResult) -> str:
        return ""

    def item_title(self, item: SearchResult):
        return item.name

    def item_link(self, item: SearchResult) -> str:
        return reverse("detail", kwargs={"judgment_uri": item.uri})

    def item_author_name(self, item: SearchResult) -> str:
        return item.author

    def item_extra_kwargs(self, item: SearchResult):
        extra_kwargs = super().item_extra_kwargs(item)
        extra_kwargs["uri"] = item.uri
        return extra_kwargs

    def item_updateddate(self, item: SearchResult) -> datetime.datetime:
        return (
            datetime.datetime.strptime(item.last_modified, "%Y-%m-%dT%H:%M:%S.%f")
            if item.last_modified
            else datetime.datetime.now()
        )
