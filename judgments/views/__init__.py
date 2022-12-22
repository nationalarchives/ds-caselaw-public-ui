import logging
import os
import re
import urllib

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
from ds_caselaw_utils import courts as all_courts
from requests_toolbelt.multipart import decoder

from judgments.models import SearchResult
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    as_integer,
    get_pdf_uri,
    has_filters,
    paginator,
    perform_advanced_search,
)


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
    pdf_uri = get_pdf_uri(judgment_uri)
    response = requests.get(pdf_uri)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type="application/pdf")

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
        context={
            "context": context,
            "courts": all_courts.get_listable_courts(),
            "tribunals": all_courts.get_listable_tribunals(),
        },
    )


def results(request):
    context = {"page_title": gettext("results.search.title")}

    try:
        params = request.GET
        query = params.get("query")
        page = str(as_integer(params.get("page"), minimum=1))
        per_page = str(
            as_integer(
                params.get("per_page"),
                minimum=1,
                maximum=MAX_RESULTS_PER_PAGE,
                default=RESULTS_PER_PAGE,
            )
        )

        if query:
            order = params.get("order", default="-relevance")
            model = perform_advanced_search(
                query=query, page=page, order=order, per_page=per_page
            )

            context["search_results"] = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["total"] = model.total
            context["paginator"] = paginator(page, model.total, per_page)
            context["query"] = query
            context["order"] = order
            context["per_page"] = per_page

            context["query_string"] = urllib.parse.urlencode(
                {"query": query, "order": order, "per_page": per_page}
            )
            context["query_params"] = {"query": query, "order": order}
            context["filtered"] = has_filters(context["query_params"])
        else:
            order = params.get("order", default="-date")
            model = perform_advanced_search(order=order, page=page, per_page=per_page)
            search_results = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["recent_judgments"] = search_results
            context["per_page"] = per_page
            context["total"] = model.total
            context["search_results"] = search_results
            context["order"] = order
            context["query_params"] = {"order": order}
            context["query_string"] = urllib.parse.urlencode(
                {"order": order, "per_page": per_page}
            )
            context["filtered"] = has_filters(context["query_params"])
            context["paginator"] = paginator(page, model.total, per_page)
        context["courts"] = all_courts.get_selectable()
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(request, template, context={"context": context})


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)
