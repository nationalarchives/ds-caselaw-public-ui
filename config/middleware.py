from urllib.parse import urlencode

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


class FeedbackLinkMiddleware:

    BASE_FEEDBACK_URL: str = (
        "https://corexmsnp4n42lf2kht3.qualtrics.com/jfe/form/SV_0lyyYAzfv9bGcyW"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We don't manipulate the response here
        return self.get_response(request)

    def process_template_response(self, request, response):
        params = {
            "full_url": request.build_absolute_uri(),
        }

        if "query" in response.context_data["context"]:
            params["search_term"] = response.context_data["context"]["query"]

        if "feedback_survey_type" in response.context_data:
            params["type"] = response.context_data["feedback_survey_type"]

        response.context_data["feedback_survey_link"] = (
            self.BASE_FEEDBACK_URL + "?" + urlencode(params)
        )
        return response
