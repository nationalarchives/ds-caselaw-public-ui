import json

from django.http import HttpResponse
from django.urls import reverse

SERVICE_DESC_URL = (
    "https://raw.githubusercontent.com/nationalarchives/ds-find-caselaw-docs/refs/heads/main/doc/openapi/public_api.yml"
)
SERVICE_DOC_URL = "https://nationalarchives.github.io/ds-find-caselaw-docs/public"


def api_catalog(request):
    api_anchor = request.build_absolute_uri(reverse("search-feed"))
    license_url = request.build_absolute_uri(reverse("open_justice_licence_v2"))

    payload = {
        "linkset": [
            {
                "anchor": api_anchor,
                "self": [{"href": api_anchor, "title": "Atom feed"}],
                "service-desc": [{"href": SERVICE_DESC_URL}],
                "service-doc": [{"href": SERVICE_DOC_URL}],
                "license": [{"href": license_url}],
            }
        ]
    }

    return HttpResponse(json.dumps(payload), content_type="application/linkset+json")
