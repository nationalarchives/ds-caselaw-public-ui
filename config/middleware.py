from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.cache import patch_cache_control


class RobotsTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        # If the response is a redirect, short-circuit adding the X-Robots-Tag
        if isinstance(response, HttpResponseRedirect):
            return response

        # If page_allow_index is True, short-circuit adding the X-Robots-Tag
        if isinstance(response, TemplateResponse) and response.context_data.get("page_allow_index", False):
            return response

        # In all other cases, assume we don't want it indexing and add the noindex X-Robots-Tag.
        response.headers["X-Robots-Tag"] = "noindex,nofollow"
        return response


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
    BASE_FEEDBACK_URL: str = "https://www.smartsurvey.co.uk/s/findcaselaw-feedback/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We don't manipulate the response here
        return self.get_response(request)

    def process_template_response(self, request, response):
        params = {
            "full_url": request.build_absolute_uri(),
        }

        if "query" in response.context_data:
            params["search_term"] = response.context_data["query"]

        if "feedback_survey_type" in response.context_data:
            params["type"] = response.context_data["feedback_survey_type"]

        if "feedback_survey_document_uri" in response.context_data:
            # TODO: update the survey to allow for generalisation to `document`
            # https://trello.com/c/l0iBFM1e/1151-update-survey-to-account-for-judgment-the-fact-that-we-have-press-summaries-as-well-as-judgments-now
            params["judgment_uri"] = response.context_data["feedback_survey_document_uri"]

        if "feedback_survey_court" in response.context_data:
            params["court"] = response.context_data["feedback_survey_court"]

        response.context_data["feedback_survey_link"] = self.BASE_FEEDBACK_URL + "?" + urlencode(params)
        return response


class StructuredBreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        if "breadcrumbs" in response.context_data:
            response.context_data["structured_breadcrumbs"] = [
                {"text": "Find Case Law", "url": request.build_absolute_uri(reverse("home"))}
            ]
            for breadcrumb in response.context_data["breadcrumbs"]:
                response.context_data["structured_breadcrumbs"].append(
                    {
                        "text": breadcrumb["text"],
                        "url": request.build_absolute_uri(breadcrumb["url"]) if "url" in breadcrumb else None,
                    }
                )

        return response
