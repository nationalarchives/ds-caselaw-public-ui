import requests
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from requests.auth import HTTPBasicAuth


def detail(request, judgment_uri):
    if judgment_uri.endswith("/"):
        judgment_uri = judgment_uri[:-1]

    response = requests.get(
        "http://localhost:8011/LATEST/documents/?uri=/" + judgment_uri + ".xml",
        auth=HTTPBasicAuth("admin", "admin"),
    )
    if response.status_code != 200:
        return HttpResponseNotFound("That judgment was not found")
    else:
        context = {"xml": response.text}
        template = loader.get_template("judgment/detail.html")
        return HttpResponse(template.render(context, request))
