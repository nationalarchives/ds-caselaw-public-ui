import json
from urllib.parse import unquote

from django.http import HttpRequest
from django.template.response import TemplateResponse


class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(
        self, request: HttpRequest, response: TemplateResponse
    ) -> TemplateResponse:
        response.context_data["showGTM"] = False
        cookie = request.COOKIES.get("cookies_policy", None)

        if cookie:
            decoder = json.JSONDecoder()
            decoded = decoder.decode(unquote(cookie))
            response.context_data["showGTM"] = decoded["usage"] or False

        return response
