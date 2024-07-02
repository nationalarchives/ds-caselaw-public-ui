from django.http import HttpResponseRedirect
from django.urls import path, register_converter

from judgments.views.browse import BrowseView
from judgments.views.index import IndexView

from . import converters, feeds
from .resolvers.document_resolver_engine import DocumentResolverEngine
from .views.advanced_search import advanced_search

register_converter(converters.YearConverter, "yyyy")
register_converter(converters.DateConverter, "date")
register_converter(converters.CourtConverter, "court")
register_converter(converters.SubdivisionConverter, "subdivision")
register_converter(converters.DocumentUriConverter, "document_uri")
register_converter(converters.FileFormatConverter, "file_format")
register_converter(converters.ComponentConverter, "component")

urlpatterns = [
    path("<court:court>", BrowseView.as_view(), name="browse"),
    path("<yyyy:year>", BrowseView.as_view(), name="browse"),
    path("<court:court>/<yyyy:year>", BrowseView.as_view(), name="browse"),
    path("<court:court>/<subdivision:subdivision>", BrowseView.as_view(), name="browse"),
    path(
        "<court:court>/<subdivision:subdivision>/<yyyy:year>",
        BrowseView.as_view(),
        name="browse",
    ),
    path("atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path("<court:court>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path("<yyyy:year>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path("<court:court>/<yyyy:year>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path(
        "transactional-licence-form",
        lambda request: HttpResponseRedirect("/computational-licence-form"),
        name="transactional-licence-form",
    ),
    path(
        "<court:court>/<subdivision:subdivision>/atom.xml",
        feeds.LatestJudgmentsFeed(),
        name="feed",
    ),
    path(
        "<court:court>/<subdivision:subdivision>/<yyyy:year>/atom.xml",
        feeds.LatestJudgmentsFeed(),
        name="feed",
    ),
    path(
        "<document_uri:document_uri>/<file_format:file_format>",
        DocumentResolverEngine.as_view(),
        name="detail",
    ),
    path(
        "<document_uri:document_uri>/<component:component>",
        DocumentResolverEngine.as_view(),
        name="detail",
    ),
    path(
        "<document_uri:document_uri>",
        DocumentResolverEngine.as_view(),
        name="detail",
    ),
    path("judgments/results", advanced_search),
    path("judgments/advanced_search", advanced_search),
    path("judgments/search", advanced_search, name="search"),
    path("", IndexView.as_view(), name="home"),
]
