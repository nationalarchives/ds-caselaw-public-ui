import requests
import xmltodict
from django.http import HttpResponse
from django.template import loader
from requests.auth import HTTPBasicAuth

from .models import Judgement


def index(request):
    judgements = Judgement.objects.all
    context = {"judgement_list": judgements}
    template = loader.get_template("judgement/index.html")
    return HttpResponse(template.render(context, request))


def detail(request, judgement_uri):
    response = requests.get(
        "http://localhost:8011/LATEST/documents/?uri=/" + judgement_uri + ".xml",
        auth=HTTPBasicAuth("rest-reader", "x"),
    )
    data = xmltodict.parse(response.text)
    context = {"xml": data}
    template = loader.get_template("judgement/detail.html")
    return HttpResponse(template.render(context, request))
