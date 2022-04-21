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
        cookie_policy = request.COOKIES.get("cookies_policy", None)
        dont_show_cookie_notice = request.COOKIES.get("dontShowCookieNotice", None)

        if cookie_policy:
            decoder = json.JSONDecoder()
            decoded = decoder.decode(unquote(cookie_policy))
            response.context_data["showGTM"] = decoded["usage"] or False

        if dont_show_cookie_notice:
            if dont_show_cookie_notice == "true":
                response.context_data["dontShowCookieNotice"] = True

        return response
