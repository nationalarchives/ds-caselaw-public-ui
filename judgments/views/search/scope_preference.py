from django.http import HttpRequest, HttpResponseBase, QueryDict
from django.utils.cache import patch_cache_control
from django.views import View

SEARCH_SCOPE_PREFERENCE_COOKIE = "search_scope_preference"
HOMEPAGE_SCOPES = ("all_courts", "higher_courts")


class SearchScopePreferenceMixin(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        params = request.GET.copy()
        is_saving_preference = params.pop("save_search_scope_preference", []) == ["1"]
        scopes = params.getlist("scope")
        request.GET = QueryDict(params.urlencode(), encoding=params.encoding)
        response = super().dispatch(request, *args, **kwargs)
        if request.method == "GET" and is_saving_preference and len(scopes) == 1 and scopes[0] in HOMEPAGE_SCOPES:
            patch_cache_control(response, private=True, no_store=True, max_age=0)
            response.set_cookie(
                SEARCH_SCOPE_PREFERENCE_COOKIE,
                scopes[0],
                max_age=365 * 24 * 60 * 60,
                secure=request.is_secure(),
            )
        return response
