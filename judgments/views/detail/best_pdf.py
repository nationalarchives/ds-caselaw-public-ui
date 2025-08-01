import logging

import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from judgments.models.document_pdf import DocumentPdf
from judgments.utils import (
    get_document_download_filename,
)


def best_pdf(request, document_uri):
    """
    Response for the data.pdf endpoint, used by data reusers

    If there's a DOCX-derived PDF in the S3 bucket, return that.
    Otherwise fall back and redirect to the weasyprint version."""
    pdf = DocumentPdf(document_uri)

    external_response = requests.get(pdf.generate_uri(), timeout=10)

    logging.debug("Response %s", external_response.status_code)

    if external_response.status_code == 200:
        response = HttpResponse(external_response.content, content_type="application/pdf")

        filename = get_document_download_filename(document_uri)

        response["Content-Disposition"] = f"attachment; filename=\"{filename}.pdf\"; filename*=UTF-8''{filename}.pdf"

        return response

    if external_response.status_code != 404:
        logging.warn(
            f"Unexpected {external_response.status_code} error on {document_uri} whilst trying to get_best_pdf"
        )
    # fall back to weasy_pdf

    return redirect(
        reverse(
            "detail",
            kwargs={"document_uri": document_uri, "file_format": "generated.pdf"},
        )
    )
