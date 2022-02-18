from django.http import Http404, HttpResponse
from django.template import loader
from lxml import etree

from marklogic import xml_tools
from marklogic.api_client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from marklogic.xml_tools import JudgmentMissingMetadataError

akn_namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}


def edit(request, judgment_uri):
    context = {"uri": judgment_uri}
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
        xml = etree.XML(bytes(judgment_xml, encoding="utf8"))
        name = xml_tools.get_metadata_name_value(xml)
        context["metadata_name"] = name
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    except JudgmentMissingMetadataError:
        context[
            "error"
        ] = "The Judgment is missing correct metadata structure and cannot be edited"
    template = loader.get_template("judgments_admin/edit.html")
    return HttpResponse(template.render({"context": context}, request))


def update(request):
    uri = request.POST["uri"]
    context = {"uri": uri}
    try:
        judgment_xml = api_client.get_judgment_xml(uri)
        xml = etree.XML(bytes(judgment_xml, encoding="utf8"))
        name = xml_tools.get_metadata_name_element(xml)
        name.set("value", request.POST["metadata_name"])
        api_client.save_judgment_xml(request.POST["uri"], xml)
        context["metadata_name"] = xml_tools.get_metadata_name_value(xml)
        context["success"] = "Judgment successfully updated"
    except MarklogicAPIError:
        context["error"] = "There was an error saving the Judgment"
    except JudgmentMissingMetadataError:
        context[
            "error"
        ] = "The Judgment is missing correct metadata structure and cannot be edited"
    template = loader.get_template("judgments_admin/edit.html")
    return HttpResponse(template.render({"context": context}, request))
