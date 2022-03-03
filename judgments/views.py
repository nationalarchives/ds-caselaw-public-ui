import math
import re

import xmltodict
from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.translation import gettext
from requests_toolbelt.multipart import decoder

import marklogic.api_client
from judgments.models import Judgment, SearchResult, SearchResults
from marklogic.api_client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)


def detail_new(request, court, year, judgment_date, subdivision=None):
    return HttpResponse(court + subdivision + str(year) + judgment_date)


def browse(request, court=None, subdivision=None, year=None):
    context = {"page_title": gettext("results.search.title")}
    queries = []

    if court:
        queries.append(court)
    if subdivision:
        queries.append(subdivision)
    if year:
        queries.append(str(year))

    query = " AND ".join(queries)

    page = request.GET.get("page") if request.GET.get("page") else "1"
    try:
        results = api_client.search_judgments(query, page)
        if type(results) == str:  # Mocked WebLogic response
            xml_results = xmltodict.parse(results)
            total = xml_results["search:response"]["@total"]
            search_results = render_mocked_results(results, with_matches=True)
            context["search_results"] = search_results
            context["total"] = total
            context["paginator"] = paginator(int(page), total)
        else:
            model = SearchResults.create_from_string(results.text)

            context["search_results"] = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["total"] = model.total
            context["paginator"] = paginator(int(page), model.total)
            context["query"] = query
    except MarklogicAPIError:
        raise Http404("Search error")

    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def detail(request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgment_xml}, request))


def xslt(request):
    params = request.GET
    judgment_uri = params.get("judgment_uri")
    try:
        judgment_xml = api_client.eval_xslt(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    template = loader.get_template("judgment/detail.html")
    return HttpResponse(template.render({"xml": judgment_xml.text}, request))


def advanced_search(request):
    params = request.GET
    query = params.get("query")
    court = params.get("court")
    judge = params.get("judge")
    party = params.get("party")
    order = params.get("order")
    date_from = params.get("from")
    date_to = params.get("to")
    page = params.get("page", 1)
    context = {}
    try:
        results = api_client.advanced_search(
            q=query,
            court=court,
            judge=judge,
            party=party,
            page=page,
            order=order,
            date_from=date_from,
            date_to=date_to,
        )
        multipart_data = decoder.MultipartDecoder.from_response(results)
        model = SearchResults.create_from_string(multipart_data.parts[0].text)

        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(int(page), model.total)
        context[
            "query_string"
        ] = f'query={str(query or "")}&court={str(court or "")}&party={str(party or "")}&judge={str(judge or "")}'
    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def detail_xml(_request, judgment_uri):
    try:
        judgment_xml = api_client.get_judgment_xml(judgment_uri)
    except MarklogicResourceNotFoundError:
        raise Http404("Judgment was not found")
    response = HttpResponse(judgment_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={judgment_uri}.xml"
    return response


def index(request):
    context = {}
    try:
        results = api_client.get_judgments_index(1)
        if type(results) == str:  # Mocked WebLogic response
            search_results = render_mocked_results(results)
        else:
            multipart_data = decoder.MultipartDecoder.from_response(results)

            search_results = format_index_results(multipart_data)

        context["recent_judgments"] = search_results

    except MarklogicResourceNotFoundError:
        raise Http404(
            "Search results not found"
        )  # TODO: This should be something else!
    template = loader.get_template("pages/home.html")
    return HttpResponse(template.render({"context": context}, request))


def results(request):
    context = {"page_title": gettext("results.search.title")}

    try:
        params = request.GET
        query = params.get("query")
        page = params.get("page") if params.get("page") else "1"

        if query:
            results = api_client.basic_search(query, page)
            if type(results) == str:  # Mocked WebLogic response
                xml_results = xmltodict.parse(results)
                total = xml_results["search:response"]["@total"]
                search_results = render_mocked_results(results, with_matches=True)
                context["search_results"] = search_results
                context["total"] = total
                context["paginator"] = paginator(int(page), total)
            else:
                model = SearchResults.create_from_string(results.text)

                context["search_results"] = [
                    SearchResult.create_from_node(result) for result in model.results
                ]
                context["total"] = model.total
                context["paginator"] = paginator(int(page), model.total)
                context["query_string"] = f"query={query}"
        else:
            results = api_client.get_judgments_index(page)
            if type(results) == str:  # Mocked WebLogic response
                xml_results = xmltodict.parse(results)
                total = xml_results["search:response"]["@total"]
                search_results = render_mocked_results(results)
                context["search_results"] = search_results
                context["total"] = total
                context["paginator"] = paginator(int(page), total)
            else:
                multipart_data = decoder.MultipartDecoder.from_response(results)

                search_metadata = xmltodict.parse(multipart_data.parts[0].text)
                total = search_metadata["search:response"]["@total"]
                search_results = format_index_results(multipart_data)

                context["total"] = total
                context["search_results"] = search_results
                context["paginator"] = paginator(int(page), total)
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return HttpResponse(template.render({"context": context}, request))


def render_mocked_results(results, with_matches=False):
    xml_results = xmltodict.parse(results)
    search_results = xml_results["search:response"]["search:result"]
    matches = ""
    if with_matches:
        matches = "<p>A test <mark>matching</mark> search result</p>"

    search_results = [
        SearchResult(
            uri=trim_leading_slash(result["@uri"]),
            neutral_citation="Fake neutral citation",
            name="Fake Judgment name",
            court="Fake court",
            date="2021-01-01",
            matches=matches,
        )
        for result in search_results
    ]
    return search_results


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
        date = model.date
        court = model.court

        search_results.append(
            SearchResult(
                uri=trim_leading_slash(filename),
                neutral_citation=neutral_citation,
                name=name,
                court=court,
                date=date,
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
