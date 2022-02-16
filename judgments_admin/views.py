from django.http import Http404, HttpResponse
from django.template import loader
from lxml import etree

from judgments.api_client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)

akn_namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}


def edit(request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
        xml = etree.XML(bytes(judgment_xml, encoding="utf8"))
        name = xml.xpath(
            "//akn:FRBRname/@value",
            namespaces=akn_namespace,
        )[0]
        context = {"metadata_name": name, "uri": judgment_uri}
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgments_admin/edit.html")
    return HttpResponse(template.render({"context": context}, request))


def update(request):
    context = {}
    try:
        judgment_xml = api_client.get_judgment_xml(request.POST["uri"])
        xml = etree.XML(bytes(judgment_xml, encoding="utf8"))
        name = xml.xpath(
            "//akn:FRBRname",
            namespaces=akn_namespace,
        )[0]
        name.set("value", request.POST["metadata_name"])
        api_client.save_judgment_xml(request.POST["uri"], xml)
        context["metadata_name"] = xml.xpath(
            "//akn:FRBRname/@value",
            namespaces=akn_namespace,
        )[0]
        context["success"] = "Judgment successfully updated"
    except MarklogicAPIError:
        context["error"] = "There was an error saving the Judgment"
    template = loader.get_template("judgments_admin/edit.html")
    return HttpResponse(template.render({"context": context}, request))
