from functools import lru_cache
from time import time

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.responses.search_response import SearchResponse
from caselawclient.search_parameters import SearchParameters
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from requests.exceptions import RequestException

from judgments.forms import AdvancedSearchForm
from judgments.utils import api_client


@lru_cache(maxsize=4)
def cached_recent_judgments(ttl_hash: int) -> SearchResponse:
    """
    This is a wrapper for caching homepage search results in memory with a maximum TTL. https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live
    """
    del ttl_hash  # ttl_hash is used to fake cache expiry with time
    return search_judgments_and_parse_response(api_client, SearchParameters(order="-date", page_size=6))


class IndexView(TemplateView):
    template_engine = "jinja"
    template_name = "pages/home.jinja"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page_canonical_url"] = self.request.build_absolute_uri(reverse("home"))
        context["page_allow_index"] = True
        context["feedback_survey_type"] = "home"
        context["form"] = AdvancedSearchForm()

        try:
            response = cached_recent_judgments(ttl_hash=round(time() / 900))
            judgments = response.results
            context["judgments"] = judgments

        except MarklogicResourceNotFoundError:
            raise Http404("Search results not found")  # TODO: This should be something else!
        except RequestException:
            context["judgments"] = []
            return context

        return context
