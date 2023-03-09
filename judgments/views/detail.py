import logging
import os

import requests
from caselawclient.Client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from requests_toolbelt.multipart import decoder

from judgments.utils import display_back_link, get_pdf_uri


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
    context = {}
    try:
        is_published = api_client.get_published(judgment_uri)
    except MarklogicAPIError:
        raise Http404("Judgment was not found")

    if is_published:
        try:
            results = api_client.eval_xslt(judgment_uri)
            multipart_data = decoder.MultipartDecoder.from_response(results)
            judgment = multipart_data.parts[0].text
            context["judgment"] = judgment
            context["page_title"] = api_client.get_judgment_name(judgment_uri)
            context["judgment_uri"] = judgment_uri

            context["pdf_size"] = get_pdf_size(judgment_uri)
            if context["pdf_size"]:  # is "" if no PDF was found
                context["pdf_uri"] = get_pdf_uri(judgment_uri)
            else:
                context["pdf_uri"] = reverse("detail_pdf", args=[judgment_uri])

            context["back_link"] = get_back_link(request)
        except MarklogicResourceNotFoundError:
            raise Http404("Judgment was not found")
        template = loader.get_template("judgment/detail.html")
        return TemplateResponse(request, template, context={"context": context})
    else:
        raise Http404("This Judgment is not available")


def detail_xml(_request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    response = HttpResponse(judgment_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={judgment_uri}.xml"
    return response


def get_pdf_size(judgment_uri):
    """Return the size of the S3 PDF for a judgment as a string in brackets, or an empty string if unavailable"""
    response = requests.head(get_pdf_uri(judgment_uri))
    content_length = response.headers.get("Content-Length", None)
    if content_length:
        filesize = filesizeformat(int(content_length))
        return f" ({filesize})"
    return ""


def get_back_link(request):
    back_link = request.META.get("HTTP_REFERER")
    if display_back_link(back_link):
        return back_link
    else:
        return None
