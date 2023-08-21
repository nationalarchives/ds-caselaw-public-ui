import logging
import os

import requests
from caselawclient.errors import DocumentNotFoundError
from caselawclient.models.documents import Document
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin

from judgments.utils import get_document_by_uri, get_pdf_uri, search_context_from_url


class NoNeutralCitationError(Exception):
    pass


# suppress weasyprint log spam
if os.environ.get("SHOW_WEASYPRINT_LOGS") != "True":
    logging.getLogger("weasyprint").handlers = []


def get_published_document_by_uri(document_uri: str) -> Document:
    try:
        document = get_document_by_uri(document_uri)
    except DocumentNotFoundError:
        raise Http404(f"Document {document_uri} was not found")

    if not document.is_published:
        raise Http404(f"Document {document_uri} is not available")
    return document


class PdfDetailView(WeasyTemplateResponseMixin, TemplateView):
    template_name = "pdf/judgment.html"
    pdf_stylesheets = [os.path.join(settings.STATIC_ROOT, "css", "judgmentpdf.css")]
    pdf_attachment = True

    def get_context_data(self, document_uri, **kwargs):
        context = super().get_context_data(**kwargs)

        document = get_published_document_by_uri(document_uri)

        self.pdf_filename = f"{document.uri}.pdf"

        context["document"] = document.content_as_html("")  # "" is most recent version

        return context


def get_best_pdf(request, document_uri):
    """
    Response for the legacy data.pdf endpoint, used by data reusers

    If there's a DOCX-derived PDF in the S3 bucket, return that.
    Otherwise fall back and redirect to the weasyprint version."""
    pdf_uri = get_pdf_uri(document_uri)
    response = requests.get(pdf_uri)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type="application/pdf")

    if response.status_code != 404:
        logging.warn(
            f"Unexpected {response.status_code} error on {document_uri} whilst trying to get_best_pdf"
        )
    # fall back to weasy_pdf
    return redirect(reverse("weasy_pdf", kwargs={"document_uri": document_uri}))


def detail(request, document_uri):
    document = get_published_document_by_uri(document_uri)

    # If the document_uri which was requested isn't the canonical URI of the document, redirect the user
    if document_uri != document.uri:
        return HttpResponseRedirect(
            reverse("detail", kwargs={"document_uri": document.uri})
        )

    context = {}

    press_summary_suffix = "/press-summary/1"
    context["document_noun"] = document.document_noun
    if document.best_human_identifier is None:
        raise NoNeutralCitationError(document.uri)
    context["judgment_ncn"] = document.best_human_identifier
    if document.document_noun == "press summary":
        linked_doc_url = document_uri.removesuffix(press_summary_suffix)
    else:
        linked_doc_url = document_uri + press_summary_suffix

    try:
        context["linked_document_uri"] = get_published_document_by_uri(
            linked_doc_url
        ).uri
    except Http404:
        context["linked_document_uri"] = ""

    context["document"] = document.content_as_html("")  # "" is most recent version
    context["document_uri"] = document.uri
    context["page_title"] = document.name
    context["pdf_size"] = get_pdf_size(document.uri)
    context["pdf_uri"] = (
        get_pdf_uri(document.uri)
        if context["pdf_size"]
        else reverse("detail_pdf", args=[document.uri])
    )

    return TemplateResponse(
        request,
        "judgment/detail.html",
        context={
            "context": context,
            "feedback_survey_type": "judgment",  # TODO: update the survey to allow for generalisation to `document`
            # https://trello.com/c/l0iBFM1e/1151-update-survey-to-account-for-judgment-the-fact-that-we-have-press-summaries-as-well-as-judgments-now
            "feedback_survey_document_uri": document.uri,
            "search_context": search_context_from_url(request.META.get("HTTP_REFERER")),
        },
    )


def detail_xml(_request, document_uri):
    document = get_published_document_by_uri(document_uri)

    document_xml = document.content_as_xml

    response = HttpResponse(document_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={document.uri}.xml"
    return response


def get_pdf_size(document_uri):
    """Return the size of the S3 PDF for a document as a string in brackets, or an empty string if unavailable"""
    response = requests.head(
        # it is possible that "" is a better value than None, but that is untested
        get_pdf_uri(document_uri),
        headers={"Accept-Encoding": None},  # type: ignore
    )
    content_length = response.headers.get("Content-Length", None)
    if response.status_code >= 400:
        return ""
    if content_length:
        filesize = filesizeformat(int(content_length))
        return f" ({filesize})"
    logging.warning(f"Unable to determine PDF size for {document_uri}")
    return " (unknown size)"
