import requests
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from requests.auth import HTTPBasicAuth

from .models import Judgement


def index(request):
    judgements = Judgement.objects.all
    context = {"judgement_list": judgements}
    template = loader.get_template("judgement/index.html")
    return HttpResponse(template.render(context, request))


def detail(request, judgement_uri):
    if (judgement_uri.endswith('/')):
        judgement_uri = judgement_uri[:-1]

    response = requests.get(
        "http://localhost:8011/LATEST/documents/?uri=/" + judgement_uri + ".xml",
        auth=HTTPBasicAuth("admin", "admin"),
    )
    if (response.status_code != 200):
        return HttpResponseNotFound("That judgment was not found")
    else:
        context = {"xml": response.text}
        template = loader.get_template("judgement/detail.html")
        return HttpResponse(template.render(context, request))
