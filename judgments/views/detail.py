import logging
import os

import requests
from caselawclient.Client import MarklogicResourceNotFoundError
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin

from judgments.utils import display_back_link, get_judgment_by_uri, get_pdf_uri


class PdfDetailView(WeasyTemplateResponseMixin, TemplateView):
    template_name = "pdf/judgment.html"
    pdf_stylesheets = [os.path.join(settings.STATIC_ROOT, "css", "judgmentpdf.css")]
    pdf_attachment = True

    def get_context_data(self, judgment_uri, **kwargs):
        context = super().get_context_data(**kwargs)

        judgment = get_judgment_by_uri(judgment_uri)

        self.pdf_filename = f"{judgment.uri}.pdf"

        context["judgment"] = judgment.content_as_html("")  # "" is most recent version

        return context


def get_best_pdf(request, judgment_uri):
    """
    Response for the legacy data.pdf endpoint, used by data reusers

    If there's a DOCX-derived PDF in the S3 bucket, return that.
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


def detail(request, judgment_uri):
    try:
        judgment = get_judgment_by_uri(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")

    if not judgment.is_published:
        raise Http404("This Judgment is not available")

    context = {}

    context["judgment"] = judgment.content_as_html("")  # "" is most recent version
    context["page_title"] = judgment.name
    context["judgment_uri"] = judgment.uri

    context["pdf_size"] = get_pdf_size(judgment.uri)
    context["pdf_uri"] = (
        get_pdf_uri(judgment.uri)
        if context["pdf_size"]
        else reverse("detail_pdf", args=[judgment.uri])
    )

    context["back_link"] = get_back_link(request)

    return TemplateResponse(
        request,
        "judgment/detail.html",
        context={
            "context": context,
            "feedback_survey_type": "judgment",
            "feedback_survey_judgment_uri": judgment.uri,
        },
    )


def detail_xml(_request, judgment_uri):
    try:
        judgment = get_judgment_by_uri(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")

    if not judgment.is_published:
        raise Http404("This Judgment is not available")

    judgment_xml = judgment.content_as_xml()

    response = HttpResponse(judgment_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={judgment.uri}.xml"
    return response


def get_pdf_size(judgment_uri):
    """Return the size of the S3 PDF for a judgment as a string in brackets, or an empty string if unavailable"""
    response = requests.head(
        # it is possible that "" is a better value than None, but that is untested
        get_pdf_uri(judgment_uri),
        headers={"Accept-Encoding": None},  # type: ignore
    )
    content_length = response.headers.get("Content-Length", None)
    if response.status_code >= 400:
        return ""
    if content_length:
        filesize = filesizeformat(int(content_length))
        return f" ({filesize})"
    logging.warning(f"Unable to determine PDF size for {judgment_uri}")
    return " (unknown size)"


def get_back_link(request):
    back_link = request.META.get("HTTP_REFERER")
    if display_back_link(back_link):
        return back_link
    else:
        return None
