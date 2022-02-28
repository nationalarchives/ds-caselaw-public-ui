from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.YearConverter, "yyyy")
register_converter(converters.DateConverter, "date")
register_converter(converters.CourtConverter, "court")
register_converter(converters.SubdivisionConverter, "subdivision")

urlpatterns = [
    path("<court:court>", views.browse, name="browse"),
    path("<yyyy:year>", views.browse, name="browse"),
    path("<court:court>/<yyyy:year>", views.browse, name="browse"),
    path("<court:court>/<subdivision:subdivision>", views.browse, name="browse"),
    path("<court:court>/<subdivision:subdivision>/<yyyy:year>", views.browse, name="browse"),

    re_path("(?P<judgment_uri>.*/.*/.*)/data.xml", views.detail_xml, name="detail"),
    re_path("(?P<judgment_uri>.*/.*/.*)/data.html", views.detail, name="detail"),
    re_path("(?P<judgment_uri>.*/.*/.*)", views.detail, name="detail"),

    path("judgments/results", views.results, name="results"),
    path("", views.index, name="home"),
]
