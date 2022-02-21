import re

import xmltodict
from django.http import Http404, HttpResponse
from django.template import loader
from lxml import etree
from requests_toolbelt.multipart import decoder

from marklogic import xml_tools
from marklogic.api_client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from marklogic.xml_tools import JudgmentMissingMetadataError


def detail(request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgment_xml}, request))


def index(request, page=1):
    context = {"page": page, "prev_page": int(page) - 1, "next_page": int(page) + 1}
    try:
        results = api_client.get_judgments_index(page)
        if type(results) == str:
            xml_results = xmltodict.parse(results)
            total = xml_results["search:response"]["@total"]
            search_results = xml_results["search:response"]["search:result"]

            search_results = [
                {
                    "uri": trim_leading_slash(result["@uri"]),
                    "neutral_citation": result["@uri"].split(".xml")[0],
                    "name": "Fake Judgment name",
                }
                for result in search_results
            ]
        else:
            multipart_data = decoder.MultipartDecoder.from_response(results)

            search_metadata = xmltodict.parse(multipart_data.parts[0].text)
            total = search_metadata["search:response"]["@total"]
            search_results = format_index_results(multipart_data)

        context["total"] = total
        context["search_results"] = search_results

    except MarklogicResourceNotFoundError:
        raise Http404("Search results not found")
    template = loader.get_template("judgment/index.html")
    return HttpResponse(template.render({"context": context}, request))


def search(request):
    context = {}
    try:
        params = request.GET
        query = params["query"]
        page = params.get("page") if params.get("page") else "1"
        results = api_client.search_judgments(query, page)
        xml = etree.XML(bytes(results.text, encoding="utf8"))
        context["total"] = xml_tools.get_search_total(xml)

        chunked_results = xml_tools.get_search_results(xml)
        search_results = [
            {
                "uri": trim_leading_slash(result.xpath("@uri")[0]).split(".xml")[0],
                "matches": xml_tools.get_search_matches(result),
            }
            for result in chunked_results
        ]
        context["search_results"] = search_results
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def format_index_results(multipart_data):
    search_results = []

    for part in multipart_data.parts[1::]:
        metadata = part.headers
        content_disposition = metadata[b"Content-Disposition"].decode("utf-8")
        filename = re.search('filename="([^"]*)"', content_disposition).group(1)
        filename = filename.split(".xml")[0]
        xml = etree.XML(bytes(part.text, encoding="utf8"))

        try:
            neutral_citation = xml_tools.get_neutral_citation(xml)
        except JudgmentMissingMetadataError:
            neutral_citation = filename

        try:
            name = xml_tools.get_metadata_name_value(xml)
        except JudgmentMissingMetadataError:
            name = "Untitled Judgment"

        search_results.append(
            {
                "uri": trim_leading_slash(filename),
                "neutral_citation": neutral_citation,
                "name": name,
            }
        )
    return search_results


def format_search_results(xml):
    return xml_tools.get_search_matches(xml)


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)


def results(request):
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({}, request))
