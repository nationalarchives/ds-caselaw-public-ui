import requests
from django.http import Http404, HttpResponse

SCHEMA_ROOT = "https://raw.githubusercontent.com/nationalarchives/ds-caselaw-marklogic/main/src/main/ml-schemas/"


def schema(request, schemafile: str):
    response = requests.get(f"{SCHEMA_ROOT}{schemafile}")
    if response.status_code != 200:
        raise Http404("Could not get schema")

    return HttpResponse(response.content, content_type="application/xml")
