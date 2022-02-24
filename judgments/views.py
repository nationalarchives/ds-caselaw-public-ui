import math
import re

import xmltodict
from django.http import Http404, HttpResponse
from django.template import loader
from requests_toolbelt.multipart import decoder

import marklogic.api_client
from judgments.models import Judgment, SearchResult, SearchResults
from marklogic.api_client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)


def detail(request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgment_xml}, request))


def index(request):
    context = {}
    params = request.GET
    page = params.get("page") if params.get("page") else "1"
    try:
        results = api_client.get_judgments_index(page)
        if type(results) == str:
            xml_results = xmltodict.parse(results)
            total = xml_results["search:response"]["@total"]
            search_results = xml_results["search:response"]["search:result"]

            search_results = [
                SearchResult(
                    uri=trim_leading_slash(result["@uri"]),
                    neutral_citation=result["@uri"].split(".xml")[0],
                    name="Fake Judgment name",
                )
                for result in search_results
            ]
        else:
            multipart_data = decoder.MultipartDecoder.from_response(results)

            search_metadata = xmltodict.parse(multipart_data.parts[0].text)
            total = search_metadata["search:response"]["@total"]
            search_results = format_index_results(multipart_data)

        context["total"] = total
        context["search_results"] = search_results
        context["paginator"] = paginator(int(page), total)

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

        model = SearchResults.create_from_string(results.text)

        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)
        context["query"] = query

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

        model = Judgment.create_from_string(part.text)

        neutral_citation = model.neutral_citation
        name = model.metadata_name

        search_results.append(
            SearchResult(
                uri=trim_leading_slash(filename),
                neutral_citation=neutral_citation,
                name=name,
            )
        )
    return search_results


def paginator(current_page, total):
    size_per_page = marklogic.api_client.RESULTS_PER_PAGE
    number_of_pages = math.ceil(int(total) / size_per_page)
    next_pages = list(range(current_page + 1, min(current_page + 10, number_of_pages)))

    return {
        "current_page": current_page,
        "has_next_page": current_page < number_of_pages,
        "next_page": current_page + 1,
        "has_prev_page": current_page > 1,
        "prev_page": current_page - 1,
        "next_pages": next_pages,
        "number_of_pages": number_of_pages,
    }


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)


def results(request):
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({}, request))
