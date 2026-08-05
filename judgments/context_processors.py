import json
from urllib.parse import unquote

from django.core.exceptions import SuspiciousOperation

from config.settings.base import env


def cookie_consent(request):
    showGTM = False
    cookie_policy = request.COOKIES.get("cookies_policy", None)

    if cookie_policy:
        decoder = json.JSONDecoder()
        try:
            decoded = decoder.decode(unquote(cookie_policy))
        except json.JSONDecodeError:
            raise SuspiciousOperation("Cookie tampered with: not valid JSON")
        showGTM = decoded["usage"] or False

    return {"showGTM": showGTM}


def environment(request):
    return {"environment": env("ROLLBAR_ENV", None)}
