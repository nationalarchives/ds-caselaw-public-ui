from django.http import HttpResponse
from django.template import loader

from judgments.api_client import ApiClient


def detail(request, judgment_uri):
    if judgment_uri.endswith("/"):
        judgment_uri = judgment_uri[:-1]

    response = ApiClient.get(judgment_uri)

    if response.status_code != 200:
        context = {"content": "That judgment was not found"}
    else:
        context = {"xml": response.text}

    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render(context, request))
