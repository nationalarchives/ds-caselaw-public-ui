import requests
from caselawclient.Client import (
    MarklogicAPIError,
    MarklogicResourceNotFoundError,
    api_client,
)
from django.http import Http404
from django.template import loader
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from requests_toolbelt.multipart import decoder

from judgments.utils import display_back_link, get_pdf_uri


def detail(request, judgment_uri):
    context = {}
    try:
        is_published = api_client.get_published(judgment_uri)
    except MarklogicAPIError:
        raise Http404("Judgment was not found")

    if is_published:
        try:
            results = api_client.eval_xslt(judgment_uri)
            multipart_data = decoder.MultipartDecoder.from_response(results)
            judgment = multipart_data.parts[0].text
            context["judgment"] = judgment
            context["page_title"] = api_client.get_judgment_name(judgment_uri)
            context["judgment_uri"] = judgment_uri
            context["pdf_size"] = get_pdf_size(judgment_uri)
            context["back_link"] = get_back_link(request)
        except MarklogicResourceNotFoundError:
            raise Http404("Judgment was not found")
        template = loader.get_template("judgment/detail.html")
        return TemplateResponse(request, template, context={"context": context})
    else:
        raise Http404("This Judgment is not available")


def get_pdf_size(judgment_uri):
    """Return the size of the S3 PDF for a judgment as a string in brackets, or an empty string if unavailable"""
    response = requests.head(get_pdf_uri(judgment_uri))
    content_length = response.headers.get("Content-Length", None)
    if content_length:
        filesize = filesizeformat(int(content_length))
        return f" ({filesize})"
    return ""


def get_back_link(request):
    back_link = request.META.get("HTTP_REFERER")
    if display_back_link(back_link):
        return back_link
    else:
        return None
