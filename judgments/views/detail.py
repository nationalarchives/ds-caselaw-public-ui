import logging
import os
import urllib
from typing import Any

import requests
from caselawclient.errors import DocumentNotFoundError, MarklogicNotPermittedError
from caselawclient.models.documents import Document, DocumentURIString
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin

from judgments.forms import AdvancedSearchForm
from judgments.models.document_pdf import DocumentPdf
from judgments.utils import (
    get_document_by_uri,
    linked_doc_title,
    linked_doc_url,
    preprocess_query,
    search_context_from_url,
)

MOST_RECENT_VERSION = DocumentURIString("")


class NoNeutralCitationError(Exception):
    pass


# suppress weasyprint log spam
if os.environ.get("SHOW_WEASYPRINT_LOGS") != "True":
    logging.getLogger("weasyprint").handlers = []


def get_published_document_by_uri(document_uri: str, cache_if_not_found: bool = False) -> Document:
    try:
        document = get_document_by_uri(document_uri, cache_if_not_found=cache_if_not_found)
        if not document:
            raise Http404(f"Document {document_uri} was not found")
    except DocumentNotFoundError:
        raise Http404(f"Document {document_uri} was not found")
    except MarklogicNotPermittedError:
        raise Http404(f"Document {document_uri} is not available")

    if not document.is_published:
        raise Http404(f"Document {document_uri} is not available")
    return document


class PdfDetailView(WeasyTemplateResponseMixin, TemplateView):
    template_name = "pdf/judgment.html"
    pdf_stylesheets = [os.path.join(settings.STATIC_ROOT, "css", "judgmentpdf.css")]
    pdf_attachment = True

    def get_context_data(self, document_uri=None, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        document = get_published_document_by_uri(document_uri)

        self.pdf_filename = f"{document.uri}.pdf"

        context["document"] = document.content_as_html(MOST_RECENT_VERSION)

        return context


def get_generated_pdf(request, document_uri):
    return PdfDetailView.as_view()(request, document_uri=document_uri)


def get_best_pdf(request, document_uri):
    """
    Response for the legacy data.pdf endpoint, used by data reusers

    If there's a DOCX-derived PDF in the S3 bucket, return that.
    Otherwise fall back and redirect to the weasyprint version."""
    pdf = DocumentPdf(document_uri)
    response = requests.get(pdf.generate_uri())
    logging.debug("Response %s", response.status_code)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type="application/pdf")

    if response.status_code != 404:
        logging.warn(f"Unexpected {response.status_code} error on {document_uri} whilst trying to get_best_pdf")
    # fall back to weasy_pdf

    return redirect(
        reverse(
            "detail",
            kwargs={"document_uri": document_uri, "file_format": "generated.pdf"},
        )
    )


def detail(request, document_uri):
    query = request.GET.get("query")
    document = get_published_document_by_uri(document_uri)
    pdf = DocumentPdf(document_uri)

    # If the document_uri which was requested isn't the canonical URI of the document, redirect the user
    if document_uri != document.uri:
        redirect_uri = reverse("detail", kwargs={"document_uri": document.uri})
        return HttpResponseRedirect(redirect_uri)

    context: dict[str, Any] = {}
    context["document_noun"] = document.document_noun
    if document.best_human_identifier is None:
        raise NoNeutralCitationError(document.uri)
    context["judgment_ncn"] = document.best_human_identifier
    if query:
        context["number_of_mentions"] = str(document.number_of_mentions(query))
        context["query"] = query

    try:
        linked_document = get_published_document_by_uri(linked_doc_url(document), cache_if_not_found=True)
        context["linked_document_uri"] = linked_document.uri
    except Http404:
        context["linked_document_uri"] = None

    context["document"] = document.content_as_html(
        MOST_RECENT_VERSION,
        query=preprocess_query(query) if query is not None else None,
    )  # "" is most recent version
    context["document_uri"] = document.uri
    context["document_canonical_url"] = request.build_absolute_uri("/" + document.uri)
    context["page_title"] = document.name
    context["pdf_size"] = f" ({filesizeformat(pdf.size)})" if pdf.size else " (unknown size)"
    context["pdf_uri"] = pdf.uri

    form: AdvancedSearchForm = AdvancedSearchForm(request.GET)

    breadcrumbs = []

    if query and form.is_valid():
        query_param_string = urllib.parse.urlencode(form.cleaned_data, doseq=True)

        breadcrumbs.append({"url": "/judgments/search?" + query_param_string, "text": f'Search results for "{query}"'})

    if document.document_noun == "press summary" and context["linked_document_uri"]:
        breadcrumbs.append(
            {
                "url": "/" + context["linked_document_uri"],
                "text": linked_doc_title(document),
            }
        )
        breadcrumbs.append(
            {
                "text": "Press Summary",
            }
        )
    else:
        breadcrumbs.append({"text": document.name})

    context["breadcrumbs"] = breadcrumbs
    context["feedback_survey_type"] = "judgment"  # TODO: update the survey to allow for generalisation to `document`
    # https://trello.com/c/l0iBFM1e/1151-update-survey-to-account-for-judgment-the-fact-that-we-have-press-summaries-as-well-as-judgments-now
    context["feedback_survey_document_uri"] = document.uri
    context["search_context"] = search_context_from_url(request.META.get("HTTP_REFERER"))

    return TemplateResponse(request, "judgment/detail.html", context=context)


def detail_xml(_request, document_uri):
    document = get_published_document_by_uri(document_uri)

    document_xml = document.content_as_xml

    response = HttpResponse(document_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={document.uri}.xml"
    return response
