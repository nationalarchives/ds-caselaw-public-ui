from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.factories import JudgmentFactory
from caselawclient.search_parameters import SearchParameters

from judgments.forms import AdvancedSearchForm
from judgments.tests.fixture_data import FakeSearchResponse
from judgments.utils import api_client

from .template_view_with_context import TemplateViewWithContext


class StyleGuideView(TemplateViewWithContext):
    template_name = "pages/style_guide.html"
    page_title = "Style Guide"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_text = "Iceland Foods Ltd v Aldi Stores Ltd"
        # document_uri =
        search_response = search_judgments_and_parse_response(
            api_client, SearchParameters(query=query_text, order="-date")
        )

        search_response = FakeSearchResponse()
        search_results = search_response.results
        document = JudgmentFactory.build(is_published=True)
        context["document"] = document
        context["judgments_for_listing"] = search_results
        context["query_text"] = query_text
        context["breadcrumbs"] = [{"url": "/style-guide", "text": "Style guide"}, {"text": "Example breadcrumbs"}]
        context["feedback_survey_type"] = "support"
        context["search_form"] = AdvancedSearchForm()
        context["menu_items"] = [
            {
                "label": "Components",
                "href": "#components",
                "children": [
                    {"label": "Breadcrumbs", "href": "#breadcrumbs"},
                    {"label": "Character count", "href": "#character-count"},
                    {"label": "Checkboxes", "href": "#checkboxes"},
                    {"label": "Details box", "href": "#details-box"},
                    {"label": "Important information box", "href": "#important-information-box"},
                    {"label": "Information text", "href": "#information-text"},
                    {"label": "Judgment header", "href": "#judgment-header"},
                    {"label": "Judgment listing", "href": "#judgment-listing"},
                    {"label": "Notification banners", "href": "#notification-banners"},
                    {"label": "Radios", "href": "#radios"},
                    {"label": "Result controls", "href": "#result-controls"},
                    {"label": "Results filters inputs", "href": "#results-filters-inputs"},
                    {"label": "Search form", "href": "#search-form"},
                    {"label": "Search term", "href": "#search-term"},
                    {"label": "Advanced search", "href": "#advanced-search"},
                    {"label": "Summary card", "href": "#summary-card"},
                    {"label": "Text input", "href": "#text-input"},
                ],
            },
            {
                "label": "Spacing",
                "href": "#spacing",
            },
            {
                "label": "Typography",
                "href": "#typography",
                "children": [
                    {"label": "Font family", "href": "#font-family"},
                    {"label": "Font sizes", "href": "#font-sizes"},
                    {"label": "Font weights", "href": "#font-weights"},
                    {"label": "Headings", "href": "#headings"},
                    {"label": "Line heights", "href": "#line-heights"},
                ],
            },
        ]
        return context
