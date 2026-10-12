from functools import lru_cache
from time import time

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.responses.search_response import SearchResponse
from caselawclient.search_parameters import SearchParameters
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.utils.cache import patch_cache_control
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView
from requests.exceptions import RequestException

from judgments.forms import AdvancedSearchForm
from judgments.search_scopes import HOMEPAGE_SCOPES, SEARCH_SCOPE_PREFERENCE_COOKIE
from judgments.utils import api_client
from judgments.utils.gtm_datalayer import GtmPageType, build_gtm_data_layer


@lru_cache(maxsize=4)
def cached_recent_judgments(ttl_hash: int) -> SearchResponse:
    """
    This is a wrapper for caching homepage search results in memory with a maximum TTL. https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live
    """
    del ttl_hash  # ttl_hash is used to fake cache expiry with time
    return search_judgments_and_parse_response(api_client, SearchParameters(order="-date", page_size=6))


@method_decorator(cache_control(private=True, no_cache=True, max_age=0), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class IndexView(TemplateView):
    template_engine = "jinja"
    template_name = "pages/home.jinja"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        scopes = request.POST.getlist("scope")
        if len(scopes) != 1 or scopes[0] not in HOMEPAGE_SCOPES:
            return HttpResponseBadRequest("Choose a valid search scope")
        params = QueryDict(mutable=True)
        params["scope"] = scopes[0]
        params["query"] = request.POST.get("query", "")
        destination = "advanced_search" if request.POST.get("action") == "advanced_search" else "search"
        response = HttpResponseRedirect(f"{reverse(destination)}?{params.urlencode()}")
        response.set_cookie(
            SEARCH_SCOPE_PREFERENCE_COOKIE,
            scopes[0],
            max_age=365 * 24 * 60 * 60,
            secure=request.is_secure(),
        )
        patch_cache_control(response, private=True, no_store=True, max_age=0)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page_canonical_url"] = self.request.build_absolute_uri(reverse("home"))
        context["page_allow_index"] = True
        context["feedback_survey_type"] = "home"
        context["active_navigation_endpoint"] = "home"
        context["form"] = AdvancedSearchForm()
        scope_preference = self.request.COOKIES.get(SEARCH_SCOPE_PREFERENCE_COOKIE)
        context["search_scope_preference"] = scope_preference if scope_preference in HOMEPAGE_SCOPES else "all_courts"
        context["gtm_data_layer"] = build_gtm_data_layer(page_type=GtmPageType.INDEX)
        context["alternates"] = [
            {
                "type": "application/atom+xml",
                "href": reverse("search-feed"),
            }
        ]

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
