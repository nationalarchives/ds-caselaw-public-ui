from typing import Optional

from django.urls import reverse
from django.views.generic import TemplateView


class TemplateViewWithContext(TemplateView):
    page_title: Optional[str] = None
    page_canonical_url_name: Optional[str] = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        if self.page_canonical_url_name:
            context["page_canonical_url"] = self.request.build_absolute_uri(reverse(self.page_canonical_url_name))
        return context
