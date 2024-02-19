from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from judgments.utils import (
    get_press_summaries_for_document_uri,
    linked_doc_title,
    press_summary_list_breadcrumbs,
)


def press_summaries(request, document_uri):
    press_summaries = get_press_summaries_for_document_uri(document_uri)

    if len(press_summaries) == 0:
        raise Http404
    elif len(press_summaries) == 1:
        return redirect(
            reverse("detail", kwargs={"document_uri": press_summaries[0].uri}),
            permanent=False,
        )

    judgement_name = linked_doc_title(press_summaries[0])
    return TemplateResponse(
        request,
        "judgment/press_summaries/list.html",
        context={
            "page_title": f"{judgement_name} - Press Summaries",
            "judgement_name": judgement_name,
            "breadcrumbs": press_summary_list_breadcrumbs(press_summaries[0]),
            "press_summaries": press_summaries,
        },
    )
