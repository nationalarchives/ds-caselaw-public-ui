import json
from urllib.parse import unquote

from django.http import HttpRequest
from django.template.response import TemplateResponse


class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Init was called") # Do not merge this line
        return self.get_response(request)

    def process_template_response(
        self, request: HttpRequest, response: TemplateResponse
    ) -> TemplateResponse:
        # Do not merge this change
        print("process_template_response was called")
        response.context_data["showGTM"] = True

        return response
