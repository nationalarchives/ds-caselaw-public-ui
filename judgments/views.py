from django.http import Http404, HttpResponse
from django.template import loader

from judgments.api_client import MarklogicResourceNotFoundError, api_client


def detail(request, judgment_uri):
    if judgment_uri.endswith("/"):
        judgment_uri = judgment_uri[:-1]
    try:
        judgement_xml = api_client.get_judgement_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgement_xml}, request))
