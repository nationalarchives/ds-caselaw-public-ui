import logging
import os

import requests
from caselawclient.errors import DocumentNotFoundError, MarklogicNotPermittedError
from caselawclient.models.documents import Document, DocumentURIString
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin

from judgments.models.document_pdf import DocumentPdf
from judgments.presenters.document_presenter import DocumentPresenter
from judgments.utils import get_document_by_uri, search_context_from_url

MOST_RECENT_VERSION = DocumentURIString("")


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
    except MarklogicNotPermittedError:
        raise Http404(f"Document {document_uri} is not available")

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
        logging.warn(
            f"Unexpected {response.status_code} error on {document_uri} whilst trying to get_best_pdf"
        )
    # fall back to weasy_pdf
    return redirect(reverse("weasy_pdf", kwargs={"document_uri": document_uri}))


def detail(request, document_uri):
    query = request.GET.get("query")
    pdf = DocumentPdf(document_uri)
    document = DocumentPresenter(
        get_published_document_by_uri(document_uri), pdf, query
    )

    # If the document_uri which was requested isn't the canonical URI of the document, redirect the user
    if document_uri != document.document_uri:
        redirect_uri = reverse("detail", kwargs={"document_uri": document.uri})
        return HttpResponseRedirect(redirect_uri)

    if document.judgment_ncn is None:
        raise NoNeutralCitationError(document.uri)

    return TemplateResponse(
        request,
        "judgment/detail.html",
        context={
            "context": {"query": query, "document": document},
            "breadcrumbs": document.breadcrumbs,
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
