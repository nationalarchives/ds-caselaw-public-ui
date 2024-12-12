import logging

import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from judgments.models.document_pdf import DocumentPdf


def best_pdf(request, document_uri):
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
        logging.warning(f"Unexpected {response.status_code} error on {document_uri} whilst trying to get_best_pdf")
    # fall back to weasy_pdf

    return redirect(
        reverse(
            "detail",
            kwargs={"document_uri": document_uri, "file_format": "generated.pdf"},
        )
    )
