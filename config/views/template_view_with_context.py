from typing import Optional

from django.urls import reverse
from django.views.generic import TemplateView

from judgments.utils.gtm_datalayer import build_gtm_data_layer


class TemplateViewWithContext(TemplateView):
    page_title: Optional[str] = None
    page_canonical_url_name: Optional[str] = None
    page_allow_index: bool = False
    # Optional GTM page_type. Subclasses that need analytics metadata should set this
    # (or assign gtm_data_layer in get_context_data); there is no blanket default.
    page_type: Optional[str] = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["page_allow_index"] = self.page_allow_index
        if self.page_type:
            context["gtm_data_layer"] = build_gtm_data_layer(page_type=self.page_type)
        if self.page_canonical_url_name:
            context["page_canonical_url"] = self.request.build_absolute_uri(reverse(self.page_canonical_url_name))
        return context
