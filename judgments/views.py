import datetime
import logging
import math
import os
import re
import urllib

import environ
import requests
from caselawclient.Client import (
    RESULTS_PER_PAGE,
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from requests_toolbelt.multipart import decoder

from judgments.fixtures.courts import courts
from judgments.fixtures.tribunals import tribunals
from judgments.models import Judgment, SearchResult

from .utils import perform_advanced_search

env = environ.Env()


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
            order="-date",
            page=int(page or 1),
        )
        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)
    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(request, template, context={"context": context})


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
    return TemplateResponse(request, template, context={"context": context})


def advanced_search(request):
    params = request.GET
    query_params = {
        "query": params.get("query"),
        "court": params.get("court"),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "neutral_citation": params.get("neutral_citation"),
        "specific_keyword": params.get("specific_keyword"),
        "order": params.get("order", ""),
        "from": params.get("from"),
        "to": params.get("to"),
    }
    page = params.get("page", 1)
    page = page if page else 1
    order = query_params["order"]
    # If there is no query, order by -date, else order by relevance
    if not order and not query_params["query"]:
        order = "-date"
    elif not order:
        order = "relevance"

    context = {}

    try:
        model = perform_advanced_search(
            query=query_params["query"],
            court=query_params["court"],
            judge=query_params["judge"],
            party=query_params["party"],
            neutral_citation=query_params["neutral_citation"],
            specific_keyword=query_params["specific_keyword"],
            page=page,
            order=order,
            date_from=query_params["from"],
            date_to=query_params["to"],
        )

        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)
        changed_queries = {
            key: value for key, value in query_params.items() if value is not None
        }
        context["query_string"] = urllib.parse.urlencode(changed_queries)
        context["query_params"] = query_params
        for key in query_params:
            context[key] = query_params[key] or ""
        context["order"] = order

    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(request, template, context={"context": context})


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


def get_best_pdf(request, judgment_uri):
    """If there's a DOCX-derived PDF in the S3 bucket, return that.
    Otherwise fall back and redirect to the weasyprint version."""
    pdf_path = f'{judgment_uri}/{judgment_uri.replace("/", "_")}.pdf'
    pdf_uri = f'https://{env("PUBLIC_ASSET_BUCKET")}.s3.{env("S3_REGION")}.amazonaws.com/{pdf_path}'
    response = requests.head(pdf_uri)
    if response.status_code == 200:
        return redirect(pdf_uri)

    if response.status_code != 404:
        logging.warn(
            f"Unexpected {response.status_code} error on {judgment_uri} whilst trying to get_best_pdf"
        )
    # fall back to weasy_pdf
    return redirect(reverse("weasy_pdf", kwargs={"judgment_uri": judgment_uri}))


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
    return TemplateResponse(
        request,
        template,
        context={"context": context, "courts": courts, "tribunals": tribunals},
    )


def results(request):
    context = {"page_title": gettext("results.search.title")}

    try:
        params = request.GET
        query = params.get("query")
        page = params.get("page") if params.get("page") else "1"
        order = params.get("order", default="-date")

        if query:
            model = perform_advanced_search(query=query, page=page, order=order)

            context["search_results"] = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["total"] = model.total
            context["paginator"] = paginator(int(page), model.total)
            context["query"] = query
            context["order"] = order
            context["query_string"] = urllib.parse.urlencode(
                {"query": query, "order": order}
            )
            context["query_params"] = {"query": query, "order": order}
        else:
            model = perform_advanced_search(order=order, page=page)
            search_results = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["recent_judgments"] = search_results

            context["total"] = model.total
            context["search_results"] = search_results
            context["order"] = order
            context["query_params"] = {"order": order}
            context["query_string"] = urllib.parse.urlencode({"order": order})
            context["paginator"] = paginator(int(page), model.total)
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(request, template, context={"context": context})


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
