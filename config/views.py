from django.views.generic import TemplateView
from django.utils.translation import gettext


class TemplateViewWithContext(TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        return {
            "context": {
                "page_title": gettext(self.page_title) if self.page_title else None
            }
        }


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_name = "pages/open_justice_licence.html"
    page_title = "openjusticelicence.title"


class TermsOfUseView(TemplateViewWithContext):
    template_name = "pages/terms_of_use.html"
    page_title = "terms.title"


class SourcesView(TemplateViewWithContext):
    template_name = "pages/sources.html"
    page_title = "judgmentsources.title"


class StructuredSearchView(TemplateViewWithContext):
    template_name = "pages/structured_search.html"
    page_title = "search.title"


class NoResultsView(TemplateViewWithContext):
    template_name = "pages/no_results.html"

