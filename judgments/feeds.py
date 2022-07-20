import datetime

from django.contrib.syndication.views import Feed
from django.http import Http404
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import SearchResult
from .utils import perform_advanced_search
from .views import paginator


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

        handler.addQuickElement(
            "link", "", {"rel": "first", "href": f'{self.feed["feed_url"]}?page=1'}
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "rel": "last",
                "href": f'{self.feed["feed_url"]}?page={str(pagination["number_of_pages"])}',
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
                    "href": f'{self.feed["feed_url"]}?page={str(pagination["next_page"])}',
                },
            )

        if pagination["has_prev_page"]:
            handler.addQuickElement(
                "link",
                "",
                {
                    "rel": "previous",
                    "href": f'{self.feed["feed_url"]}?page={str(pagination["prev_page"])}',
                },
            )


class LatestJudgmentsFeed(Feed):
    feed_type = JudgmentAtomFeed
    author_name = "The National Archives"

    def get_object(self, request, court=None, subdivision=None, year=None):
        court_query = "/".join(filter(lambda x: x is not None, [court, subdivision]))
        slugs = filter(lambda x: x is not None, [court, subdivision, year])
        slug = "/".join([str(s) for s in slugs])
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            # e.g. the user provided ?page= or ?page=jam
            raise Http404
        order = request.GET.get("order", "-date")
        model = perform_advanced_search(
            court=court_query if court_query else None,
            date_from=datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
            if year
            else None,
            date_to=datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
            if year
            else None,
            order=order,
            page=page,
        )
        return {"slug": slug, "model": model, "page": page, "order": order}

    def title(self, obj):
        if not obj["slug"]:
            return "Latest judgments"

        return f'Latest judgments for {obj.get("slug", "/")}'

    def link(self, obj):
        page = obj.get("page", 1)
        return f"/{obj['slug']}/atom.xml/?page={page}&order={obj.get('order')}"

    def items(self, obj):
        return [
            SearchResult.create_from_node(result) for result in obj["model"].results
        ]

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
        extra_kwargs["content_hash"] = item.content_hash
        return extra_kwargs

    def item_updateddate(self, item: SearchResult) -> datetime.datetime:
        date_string = item.transformation_date or "1970-01-01T00:00:00.000"
        return datetime.datetime.fromisoformat(date_string)

    def item_pubdate(self, item: SearchResult) -> datetime.datetime:
        date_string = item.date or "1970-01-01"
        return datetime.datetime.fromisoformat(date_string)

    def feed_extra_kwargs(self, obj):
        extra_kwargs = super().item_extra_kwargs(obj)
        extra_kwargs["total"] = int(obj["model"].total)
        extra_kwargs["page"] = obj["page"]
        return extra_kwargs
