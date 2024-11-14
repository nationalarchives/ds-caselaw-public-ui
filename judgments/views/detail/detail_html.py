import logging
import os
import urllib
from typing import Any

from django.http import Http404, HttpResponseRedirect
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from django.urls import reverse
from lxml import html as html_parser

from judgments.forms import AdvancedSearchForm
from judgments.models.document_pdf import DocumentPdf
from judgments.utils import (
    get_published_document_by_uri,
    linked_doc_title,
    linked_doc_url,
    preprocess_query,
    search_context_from_url,
)


class NoNeutralCitationError(Exception):
    pass


# suppress weasyprint log spam
if os.environ.get("SHOW_WEASYPRINT_LOGS") != "True":
    logging.getLogger("weasyprint").handlers = []


def number_of_mentions(content: str, query: str) -> int:
    tree = html_parser.fromstring(content.encode("utf-8"))
    return len(tree.findall(".//mark"))


def detail_html(request, document_uri):
    query = request.GET.get("query")

    context: dict[str, Any] = {}

    if query:
        cleaned_search_query = preprocess_query(query)
        document = get_published_document_by_uri(document_uri, search_query=cleaned_search_query)
        context["query"] = query
        context["number_of_mentions"] = number_of_mentions(document.body.content_as_html(), cleaned_search_query)
    else:
        document = get_published_document_by_uri(document_uri)

    pdf = DocumentPdf(document_uri)

    # If the document_uri which was requested isn't the canonical URI of the document, redirect the user
    if document_uri != document.uri:
        redirect_uri = reverse("detail", kwargs={"document_uri": document.uri})
        return HttpResponseRedirect(redirect_uri)

    if document.best_human_identifier is None:
        raise NoNeutralCitationError(document.uri)

    try:
        linked_document_uri = linked_doc_url(document)
        linked_document = get_published_document_by_uri(linked_document_uri, cache_if_not_found=True)
        context["linked_document_uri"] = linked_document.uri
    except Http404:
        context["linked_document_uri"] = None

    context["document_html"] = document.body.content_as_html()
    context["pdf_size"] = f" ({filesizeformat(pdf.size)})" if pdf.size else " (unknown size)"

    form: AdvancedSearchForm = AdvancedSearchForm(request.GET)

    breadcrumbs = []

    if query and form.is_valid():
        query_param_string = urllib.parse.urlencode(form.cleaned_data, doseq=True)

        breadcrumbs.append({"url": "/judgments/search?" + query_param_string, "text": f'Search results for "{query}"'})

    if document.document_noun == "press summary" and context["linked_document_uri"]:
        breadcrumbs.append(
            {
                "url": "/" + context["linked_document_uri"],
                "text": linked_doc_title(document),
            }
        )
        breadcrumbs.append(
            {
                "text": "Press Summary",
            }
        )
    else:
        breadcrumbs.append({"text": document.body.name})

    context["breadcrumbs"] = breadcrumbs
    context["feedback_survey_type"] = "judgment"  # TODO: update the survey to allow for generalisation to `document`
    # https://trello.com/c/l0iBFM1e/1151-update-survey-to-account-for-judgment-the-fact-that-we-have-press-summaries-as-well-as-judgments-now
    context["search_context"] = search_context_from_url(request.META.get("HTTP_REFERER"))
    context["document"] = document
    context["page_canonical_url"] = document.public_uri
    context["document_canonical_url"] = request.build_absolute_uri("/" + document.uri)
    context["feedback_survey_document_uri"] = document.uri  # TODO: Remove this from context
    context["page_title"] = document.body.name  # TODO: Remove this from context
    context["pdf_uri"] = pdf.uri  # TODO: Remove this from context

    return TemplateResponse(request, "judgment/detail.html", context=context)
