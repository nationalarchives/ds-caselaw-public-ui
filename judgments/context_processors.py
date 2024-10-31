import json
from typing import Union
from urllib.parse import unquote

from django.core.exceptions import SuspiciousOperation

from config.settings.base import env


def cookie_consent(request):
    showGTM = False
    dontShowCookieNotice = False
    cookie_policy = request.COOKIES.get("cookies_policy", None)
    dont_show_cookie_notice = request.COOKIES.get("dontShowCookieNotice", None)

    if cookie_policy:
        decoder = json.JSONDecoder()
        try:
            decoded = decoder.decode(unquote(cookie_policy))
        except json.JSONDecodeError:
            raise SuspiciousOperation("Cookie tampered with: not valid JSON")
        showGTM = decoded["usage"] or False

    if dont_show_cookie_notice == "true":
        dontShowCookieNotice = True

    return {"showGTM": showGTM, "dontShowCookieNotice": dontShowCookieNotice}


def environment(request):
    return {"environment": env("ROLLBAR_ENV", None)}
