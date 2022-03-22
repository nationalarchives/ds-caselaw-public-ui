import datetime
import math
import os
import re

from caselawclient.Client import (
    RESULTS_PER_PAGE,
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.translation import gettext
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from requests_toolbelt.multipart import decoder

from judgments.models import Judgment, SearchResult, SearchResults


def browse(request, court=None, subdivision=None, year=None):
    court_query = "/".join(filter(lambda x: x is not None, [court, subdivision]))
    page = request.GET.get("page", 1)
    context = {}

    try:
        model = perform_advanced_search(
            court=court_query if court_query else None,
            date_from=datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
            if year
            else None,
            date_to=datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
            if year
            else None,
        )
        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)
    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def detail(request, judgment_uri):
    context = {}
    try:
        results = api_client.eval_xslt(judgment_uri)
        xml_results = api_client.get_judgment_xml(judgment_uri)
        multipart_data = decoder.MultipartDecoder.from_response(results)
        judgment = multipart_data.parts[0].text
        model = Judgment.create_from_string(xml_results)
        context["judgment"] = judgment
        context["page_title"] = model.metadata_name
        context["judgment_uri"] = judgment_uri
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"context": context}, request))


def advanced_search(request):
    params = request.GET
    query_params = {
        "query": params.get("query"),
        "court": params.get("court"),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "order": params.get("order"),
        "from": params.get("from"),
        "to": params.get("to"),
    }
    page = params.get("page", 1)
    context = {}

    try:
        model = perform_advanced_search(
            query=query_params["query"],
            court=query_params["court"],
            judge=query_params["judge"],
            party=query_params["party"],
            page=page,
            order=query_params["order"],
            date_from=query_params["from"],
            date_to=query_params["to"],
        )

        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)

        context["query_string"] = "&".join(
            [f'{key}={query_params[key] or ""}' for key in query_params]
        )

    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def detail_xml(_request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    response = HttpResponse(judgment_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={judgment_uri}.xml"
    return response


class PdfDetailView(WeasyTemplateResponseMixin, TemplateView):
    template_name = "pdf/judgment.html"
    pdf_stylesheets = [os.path.join(settings.STATIC_ROOT, "css", "judgmentpdf.css")]
    pdf_attachment = True

    def dispatch(self, request, *args, **kwargs):
        self.pdf_filename = f'{kwargs["judgment_uri"]}.pdf'

        return super(PdfDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, judgment_uri, **kwargs):
        context = super().get_context_data(**kwargs)

        results = api_client.eval_xslt(judgment_uri)
        multipart_data = decoder.MultipartDecoder.from_response(results)
        context["judgment"] = multipart_data.parts[0].text

        return context


def index(request):
    context = {}
    try:
        model = perform_advanced_search(order="-date")
        search_results = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["recent_judgments"] = search_results

    except MarklogicResourceNotFoundError:
        raise Http404(
            "Search results not found"
        )  # TODO: This should be something else!
    template = loader.get_template("pages/home.html")
    return HttpResponse(template.render({"context": context}, request))


def results(request):
    context = {"page_title": gettext("results.search.title")}

    try:
        params = request.GET
        query = params.get("query")
        page = params.get("page") if params.get("page") else "1"

        if query:
            model = perform_advanced_search(query=query, page=page)

            context["search_results"] = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["total"] = model.total
            context["paginator"] = paginator(int(page), model.total)
            context["query_string"] = f"query={query}"
        else:
            model = perform_advanced_search(order="-date", page=page)
            search_results = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["recent_judgments"] = search_results

            context["total"] = model.total
            context["search_results"] = search_results
            context["paginator"] = paginator(int(page), model.total)
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def paginator(current_page, total):
    size_per_page = RESULTS_PER_PAGE
    number_of_pages = math.ceil(int(total) / size_per_page)
    next_pages = list(range(current_page + 1, min(current_page + 10, number_of_pages)))

    return {
        "current_page": current_page,
        "has_next_page": current_page < number_of_pages,
        "next_page": current_page + 1,
        "has_prev_page": current_page > 1,
        "prev_page": current_page - 1,
        "next_pages": next_pages,
        "number_of_pages": number_of_pages,
    }


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)


def perform_advanced_search(
    query=None,
    court=None,
    judge=None,
    party=None,
    order=None,
    date_from=None,
    date_to=None,
    page=1,
):
    response = api_client.advanced_search(
        q=query,
        court=court,
        judge=judge,
        party=party,
        page=page,
        order=order,
        date_from=date_from,
        date_to=date_to,
    )
    multipart_data = decoder.MultipartDecoder.from_response(response)
    return SearchResults.create_from_string(multipart_data.parts[0].text)
