from typing import Optional

from caselawclient.identifier_resolution import IdentifierResolutions
from caselawclient.models.documents import DocumentURIString
from django.views.generic.base import TemplateView
import warnings

class DisambiguationWarning(Warning):
    """An identifier URL has many possible resolutions"""

class DisambiguationView(TemplateView):
    template_name = "judgment/disambiguation.html"

    def get_context_data(
        self, uri: DocumentURIString, resolutions: IdentifierResolutions, file_format: Optional[str], **kwargs
    ):
        msg = f"Multiple resolutions for slug {uri}"
        warnings.warn(DisambiguationWarning(msg))

        for resolution in resolutions:
        context = super().get_context_data(**kwargs)
        context["uri"] = uri
        context["resolutions"] = resolutions
        context["file_format"] = f"/{file_format}" if file_format else ""
        
        return context
