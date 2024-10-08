from typing import Optional

from django.urls import reverse
from django.views.generic import TemplateView


class TemplateViewWithContext(TemplateView):
    page_title: Optional[str] = None
    page_canonical_url_name: Optional[str] = None
    page_allow_index: bool = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["page_allow_index"] = self.page_allow_index
        if self.page_canonical_url_name:
            context["page_canonical_url"] = self.request.build_absolute_uri(reverse(self.page_canonical_url_name))
        return context
