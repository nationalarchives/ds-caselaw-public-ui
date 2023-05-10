from django.urls import path, register_converter

from . import converters, feeds
from .views.advanced_search import advanced_search
from .views.browse import browse
from .views.detail import PdfDetailView, detail, detail_xml, get_best_pdf
from .views.index import index
from .views.results import results

register_converter(converters.YearConverter, "yyyy")
register_converter(converters.DateConverter, "date")
register_converter(converters.CourtConverter, "court")
register_converter(converters.SubdivisionConverter, "subdivision")
register_converter(converters.JudgmentConverter, "judgment")

urlpatterns = [
    path("<court:court>", browse, name="browse"),
    path("<yyyy:year>", browse, name="browse"),
    path("<court:court>/<yyyy:year>", browse, name="browse"),
    path("<court:court>/<subdivision:subdivision>", browse, name="browse"),
    path(
        "<court:court>/<subdivision:subdivision>/<yyyy:year>",
        browse,
        name="browse",
    ),
    path("atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path("<court:court>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path("<yyyy:year>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"),
    path(
        "<court:court>/<yyyy:year>/atom.xml", feeds.LatestJudgmentsFeed(), name="feed"
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
    path("<judgment:judgment_uri>/data.pdf", get_best_pdf, name="detail_pdf"),
    path(
        "<judgment:judgment_uri>/generated.pdf",
        PdfDetailView.as_view(),
        name="weasy_pdf",
    ),
    path("<judgment:judgment_uri>/data.xml", detail_xml, name="detail_xml"),
    path("<judgment:judgment_uri>/data.html", detail, name="detail"),
    path("<judgment:judgment_uri>", detail, name="detail"),
    path("judgments/results", results, name="results"),
    path("judgments/advanced_search", advanced_search, name="advanced_search"),
    path("", index, name="home"),
]
