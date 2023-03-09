from django.utils.cache import patch_cache_control


class CacheHeaderMiddleware:
    # via https://docs.djangoproject.com/en/4.1/topics/http/middleware/

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        patch_cache_control(response, max_age=15 * 60, public=True)

        # Code to be executed for each request/response after
        # the view is called.

        return response
