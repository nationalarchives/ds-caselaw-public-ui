import datetime

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import SearchResult
from .utils import perform_advanced_search


class LatestJudgmentsFeed(Feed):
    feed_type = Atom1Feed

    def get_object(self, request, court=None, subdivision=None, year=None):
        return {"court": court, "subdivision": subdivision, "year": year}

    def title(self, obj):
        return (
            f'Latest judgments for /{obj["court"]}/{obj["subdivision"]}/{obj["year"]}'
        )

    def link(self, obj):
        return "/" + "/".join(
            filter(
                lambda x: x is not None,
                [obj["court"], obj["subdivision"], str(obj["year"])],
            )
        )

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
        )

        return [SearchResult.create_from_node(result) for result in model.results]

    def item_description(self, item: SearchResult) -> str:
        return ""

    def item_title(self, item: SearchResult):
        return item.name

    def item_link(self, item: SearchResult) -> str:
        return reverse("detail", kwargs={"judgment_uri": item.uri})
