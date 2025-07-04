import logging
import os
from typing import Any

from caselawclient.models.documents import DocumentURIString
from django.conf import settings
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin

from judgments.utils import get_document_download_filename, get_published_document_by_uri

# suppress weasyprint log spam
if os.environ.get("SHOW_WEASYPRINT_LOGS") != "True":
    logging.getLogger("weasyprint").handlers = []


class PdfDetailView(WeasyTemplateResponseMixin, TemplateView):
    template_name = "pdf/document.html"
    pdf_stylesheets = [os.path.join(settings.STATIC_ROOT, "css", "document_pdf.css")]
    pdf_attachment = True

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        document_uri = DocumentURIString(kwargs["document_uri"])
        filename = get_document_download_filename(document_uri)
        document = get_published_document_by_uri(document_uri)

        self.pdf_filename = f"{filename}.pdf"

        context["document"] = document.content_as_html()

        return context


def generated_pdf(request, document_uri):
    return PdfDetailView.as_view()(request, document_uri=document_uri)
