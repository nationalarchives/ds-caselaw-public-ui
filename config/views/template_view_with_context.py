from django.views.generic import TemplateView
from django.utils.translation import gettext


class TemplateViewWithContext(TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext(self.page_title) if self.page_title else None
        return context
