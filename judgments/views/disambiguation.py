from typing import Optional

from caselawclient.identifier_resolution import IdentifierResolutions
from caselawclient.models.documents import DocumentURIString
from django.views.generic.base import TemplateView


class DisambiguationView(TemplateView):
    template_name = "judgment/disambiguation.html"

    def get_context_data(
        self, uri: DocumentURIString, resolutions: IdentifierResolutions, file_format: Optional[str], **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["uri"] = uri
        context["resolutions"] = resolutions
        context["file_format"] = f"/{file_format}" or ""

        return context
