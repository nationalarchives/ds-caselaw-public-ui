import re

import xmltodict
from django.http import Http404, HttpResponse
from django.template import loader
from lxml import etree
from requests_toolbelt.multipart import decoder

from judgments.api_client import MarklogicResourceNotFoundError, api_client


def detail(request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgment_xml}, request))


def index(request, page=1):
    try:
        results = api_client.get_judgment_search_results(page)
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

            search_results = []

            for part in multipart_data.parts[1::]:
                metadata = part.headers
                content_disposition = metadata[b"Content-Disposition"].decode("utf-8")
                filename = re.search('filename="([^"]*)"', content_disposition).group(1)
                filename = filename.split(".xml")[0]
                xml = etree.XML(bytes(part.text, encoding="utf8"))
                neutral_citation = xml.xpath(
                    "//akn:neutralCitation",
                    namespaces={
                        "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                    },
                )
                name = xml.xpath(
                    "//akn:FRBRname/@value",
                    namespaces={
                        "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                    },
                )

                if not neutral_citation:
                    neutral_citation = filename
                else:
                    neutral_citation = neutral_citation[0].text

                if not name:
                    name = "Untitled Judgment"
                else:
                    name = name[0]

                search_results.append(
                    {
                        "uri": trim_leading_slash(filename),
                        "neutral_citation": neutral_citation,
                        "name": name,
                    }
                )

        context = {
            "total": total,
            "search_results": search_results,
            "page": page,
            "prev_page": int(page) - 1,
            "next_page": int(page) + 1,
        }

    except MarklogicResourceNotFoundError:
        raise Http404("Search results not found")
    template = loader.get_template("judgment/index.html")
    return HttpResponse(template.render({"context": context}, request))


def source():
    return


def structured_search():
    return


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)
