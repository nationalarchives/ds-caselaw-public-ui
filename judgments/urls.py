from django.urls import path, re_path, register_converter

from . import converters, feeds, views

register_converter(converters.YearConverter, "yyyy")
register_converter(converters.DateConverter, "date")
register_converter(converters.CourtConverter, "court")
register_converter(converters.SubdivisionConverter, "subdivision")

urlpatterns = [
    path("<court:court>", views.browse, name="browse"),
    path("<yyyy:year>", views.browse, name="browse"),
    path("<court:court>/<yyyy:year>", views.browse, name="browse"),
    path("<court:court>/<subdivision:subdivision>", views.browse, name="browse"),
    path(
        "<court:court>/<subdivision:subdivision>/<yyyy:year>",
        views.browse,
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
    re_path(
        r"(?P<judgment_uri>.*/\d{4}/\d+)/data.pdf",
        views.get_best_pdf,
        name="detail_pdf",
    ),
    re_path(
        r"(?P<judgment_uri>.*/\d{4}/\d+)/generated.pdf",
        views.PdfDetailView.as_view(),
        name="weasy_pdf",
    ),
    re_path(
        r"(?P<judgment_uri>.*/\d{4}/\d+)/data.xml", views.detail_xml, name="detail_xml"
    ),
    re_path(r"(?P<judgment_uri>.*/\d{4}/\d+)/data.html", views.detail, name="detail"),
    re_path(r"(?P<judgment_uri>.*/\d{4}/\d+)", views.detail, name="detail"),
    path("judgments/results", views.results, name="results"),
    path("judgments/advanced_search", views.advanced_search, name="advanced_search"),
    path("", views.index, name="home"),
]
