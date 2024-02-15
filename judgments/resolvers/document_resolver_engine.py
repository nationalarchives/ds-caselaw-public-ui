from typing import Optional

from django.http.request import HttpRequest
from django.views.generic import View

from judgments.views.detail import detail, detail_xml, get_best_pdf, get_generated_pdf
from judgments.views.press_summaries import press_summaries


class DocumentResolverEngine(View):
    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
        component: Optional[str] = None,
    ):
        fileformat_lookup = {
            "data.pdf": get_best_pdf,
            "generated.pdf": get_generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail,
        }
        component_lookup = {
            "press-summary": press_summaries,
        }
        if file_format:
            return fileformat_lookup[file_format](request, document_uri)

        if component:
            return component_lookup[component](request, document_uri)

        return detail(request, document_uri)
