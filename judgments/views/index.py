from caselawclient.Client import MarklogicResourceNotFoundError
from django.http import Http404
from django.template import loader
from django.template.response import TemplateResponse
from ds_caselaw_utils import courts as all_courts

from judgments.models import SearchResult
from judgments.utils import perform_advanced_search


def index(request):
    context = {}
    try:
        model = perform_advanced_search(order="-date")
        search_results = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["recent_judgments"] = search_results

    except MarklogicResourceNotFoundError:
        raise Http404(
            "Search results not found"
        )  # TODO: This should be something else!
    template = loader.get_template("pages/home.html")
    return TemplateResponse(
        request,
        template,
        context={
            "context": context,
            "courts": all_courts.get_listable_courts(),
            "tribunals": all_courts.get_listable_tribunals(),
            "feedback_survey_type": "home",
        },
    )
