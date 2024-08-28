import json
from typing import Union
from urllib.parse import unquote

from django.core.exceptions import SuspiciousOperation
from waffle import flag_is_active
from waffle.models import Flag

from config.settings.base import env


def waffle_flags(request):
    """variant_homepage is the A/B flag, randomly generated.
    v1/v2/v3 are the different treatment flags, toggled on or off.
    We enforce that no more than one treatment may be active at a time,
    and that variant_homepage is only true if a treatment is selected.
    """

    context: dict[str, Union[bool, dict[str, bool]]] = {}

    if not flag_is_active(request, "variant_homepage"):
        context = {"variant_homepage": False, "v1_homepage": False, "v2_homepage": False, "v3_homepage": False}
    elif flag_is_active(request, "v1_homepage"):
        context = {"variant_homepage": True, "v1_homepage": True, "v2_homepage": False, "v3_homepage": False}
    elif flag_is_active(request, "v2_homepage"):
        context = {"variant_homepage": True, "v1_homepage": False, "v2_homepage": True, "v3_homepage": False}
    elif flag_is_active(request, "v3_homepage"):
        context = {"variant_homepage": True, "v1_homepage": False, "v2_homepage": False, "v3_homepage": True}
    else:
        context = {"variant_homepage": False, "v1_homepage": False, "v2_homepage": False, "v3_homepage": False}

    flags = {}
    for flag in Flag.objects.all():
        flags[flag.name] = flag.is_active(request)

    context.update({"waffle_flags": flags})

    return context


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
