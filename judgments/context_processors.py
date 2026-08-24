import json
from urllib.parse import unquote

from django.core.exceptions import SuspiciousOperation
from django.http.request import split_domain_port

from config.settings.base import env


def cookie_domain_from_host(host):
    hostname, _port = split_domain_port(host or "")
    hostname = hostname.lower().rstrip(".").strip("[]")
    hostname_parts = [part for part in hostname.split(".") if part]

    if not hostname or len(hostname_parts) == 1 or ":" in hostname or all(part.isdigit() for part in hostname_parts):
        return hostname

    root_domain_part_count = 3 if len(hostname_parts[-1]) == 2 else 2
    return f".{'.'.join(hostname_parts[-root_domain_part_count:])}"


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


def cookie_settings(request):
    return {"cookie_domain": cookie_domain_from_host(request.get_host())}


def environment(request):
    return {"environment": env("ROLLBAR_ENV", None)}
