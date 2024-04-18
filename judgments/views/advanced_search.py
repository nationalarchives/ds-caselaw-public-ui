import urllib

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from ds_caselaw_utils import courts as all_courts

from judgments.forms import AdvancedSearchForm
from judgments.models.search_form_errors import SearchFormErrors
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    api_client,
    as_integer,
    has_filters,
    paginator,
    parse_date_parameter,
    preprocess_query,
    process_court_facets,
    process_year_facets,
    show_no_exact_ncn_warning,
)

def _get_search_parameters(query_text:str, params: dict, form: AdvancedSearchForm):
    return SearchParameters(
        query=query_text,
        court=params.get("court", ""),
        judge=form.fields.get("judge", ""),
        party=form.fields.get("party", ""),
        page=params.get("page", "1"),
        order=params.get("order", "-date"),
        date_from=form.fields.get("from"),
        date_to=form.fields.get("to", ""),
        page_size=params.get("per_page", 10),
        )


def advanced_search(request):
    # TODO: You should be able to just split the form in the templates using form.field, they don't have to be wrapped in inputs or forms in html.
    # TODO: Probably worth just changing this back to a GET request
    if request.method == "GET":
        form = AdvancedSearchForm(request.GET)
        params = request.GET

        """
        Form should be valid unless there is a critical issue
        with the submission (i.e. Month > 12)
        """
        if form.is_valid():
            try:
                context: dict = {}
                query_text: str = params.get("query", "")

                search_parameters: SearchParameters = _get_search_parameters(preprocess_query(query_text), params, form)
                
                search_response = search_judgments_and_parse_response(
                    api_client, search_parameters
                )

                court_facets = {}
                year_facets = {}
                """
                if search_parameters.query:
                    unprocessed_facets, court_facets = process_court_facets(
                        search_response.facets, params["query_params"].get("court", {})
                    )
                    unprocessed_facets, year_facets = process_year_facets(
                        unprocessed_facets
                    )
                """
                
                page: str = str(as_integer("1", minimum=1))
                per_page: str = str(
                    as_integer(
                        params.get("per_page", "10"),
                        minimum=1,
                        maximum=MAX_RESULTS_PER_PAGE,
                        default=RESULTS_PER_PAGE,
                    )
                )
                order=params.get("order", "-date")

                # TODO: Maybe separate this dictionary into it's component parts?
                context["court_facets"] = court_facets
                context["year_facets"] = year_facets
                context["search_results"] = search_response.results
                context["total"] = search_response.total
                context["paginator"] = paginator(params.get("page", "1"), search_response.total, per_page)
                changed_queries = {
                    key: value for key, value in params.items() if value is not None
                }
                context["query_string"] = urllib.parse.urlencode(
                    changed_queries, doseq=True
                )
                context["order"] = order
                context["per_page"] = per_page
                context["filtered"] = has_filters(params)
                context["page_title"] = _("results.search.title")
                context["show_no_exact_ncn_warning"] = show_no_exact_ncn_warning(
                    search_response.results, query_text, page
                )

            except MarklogicResourceNotFoundError:
                raise Http404("Search failed")
            # If we have a search query, stick it in the breadcrumbs. Otherwise, don't bother.
            if query_text:
                breadcrumbs = [{"text": f'Search results for "{query_text}"'}]
            else:
                breadcrumbs = [{"text": "Search results"}]
            return TemplateResponse(
                request,
                "judgment/results.html",
                context={
                    "form": form,
                    "context": context,
                    "breadcrumbs": breadcrumbs,
                    "feedback_survey_type": "structured_search",
                }
            )
        else:
            return TemplateResponse(
                request, "pages/structured_search.html", {"form": form}
        )
    else:
        form = AdvancedSearchForm()
    return render(request, "pages/structured_search.html", {"form": form})

def advanced_search_remove(request):
    params = request.GET
    errors = SearchFormErrors()

    from_date, from_parser_errors = parse_date_parameter(
        params,
        "from",
    )
    to_date, to_parser_errors = parse_date_parameter(
        params,
        "to",
        default_to_last=True,
    )
    parser_errors = {**from_parser_errors, **to_parser_errors}

    if to_date is not None and from_date is not None and to_date < from_date:
        errors.add_error(
            _("search.errors.to_before_from_headline"),
            "to_date",
            _("search.errors.to_before_from_detail"),
        )

    query_params = {
        "query": params.get("query", ""),
        "court": params.getlist("court"),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "order": params.get("order", ""),
        "from": from_date,
        "from_day": params.get("from_day"),
        "from_month": params.get("from_month"),
        "from_year": params.get("from_year"),
        "to": to_date,
        "to_day": params.get("to_day"),
        "to_month": params.get("to_month"),
        "to_year": params.get("to_year"),
        "per_page": params.get("per_page"),
    }

    query_text = query_params["query"]
    page = str(as_integer(params.get("page"), minimum=1))
    per_page = str(
        as_integer(
            params.get("per_page"),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
            default=RESULTS_PER_PAGE,
        )
    )

    order = query_params["order"]
    # If there is no query, order by -date, else order by relevance
    if not order and not query_text:
        order = "-date"
    elif not order:
        order = "relevance"

    context = {
        "errors": errors,
        "query": query_text,
        "courts": all_courts.get_grouped_selectable_courts(),
        "tribunals": all_courts.get_grouped_selectable_tribunals(),
        "query_params": query_params,
    }

    for key in query_params:
        context[key] = query_params[key] or ""

    if errors.has_errors():
        return TemplateResponse(
            request, "pages/structured_search.html", context={"context": context}
        )
    else:
        try:
            query_without_stop_words = preprocess_query(query_text)
            search_parameters = SearchParameters(
                query=query_without_stop_words,
                court=",".join(query_params["court"]),
                judge=query_params["judge"],
                party=query_params["party"],
                page=int(page),
                order=order,
                date_from=query_params["from"],
                date_to=query_params["to"],
                page_size=int(per_page),
            )
            search_response = search_judgments_and_parse_response(
                api_client, search_parameters
            )

            court_facets = {}
            year_facets = {}

            if search_parameters.query:
                unprocessed_facets, court_facets = process_court_facets(
                    search_response.facets, context["query_params"].get("court")
                )
                unprocessed_facets, year_facets = process_year_facets(
                    unprocessed_facets
                )

            # TODO: Maybe separate this dictionary into it's component parts?
            context["parser_errors"] = parser_errors
            context["court_facets"] = court_facets
            context["year_facets"] = year_facets
            context["search_results"] = search_response.results
            context["total"] = search_response.total
            context["paginator"] = paginator(page, search_response.total, per_page)
            changed_queries = {
                key: value for key, value in query_params.items() if value is not None
            }
            context["query_string"] = urllib.parse.urlencode(
                changed_queries, doseq=True
            )
            context["order"] = order
            context["per_page"] = per_page
            context["filtered"] = has_filters(context["query_params"])
            context["page_title"] = _("results.search.title")
            context["show_no_exact_ncn_warning"] = show_no_exact_ncn_warning(
                search_response.results, query_text, page
            )

        except MarklogicResourceNotFoundError:
            raise Http404("Search failed")  # TODO: This should be something else!

        # If we have a search query, stick it in the breadcrumbs. Otherwise, don't bother.
        if query_text:
            breadcrumbs = [{"text": f'Search results for "{query_text}"'}]
        else:
            breadcrumbs = [{"text": "Search results"}]
        return TemplateResponse(
            request,
            "judgment/results.html",
            context={
                "context": context,
                "breadcrumbs": breadcrumbs,
                "feedback_survey_type": "structured_search",
            },
        )
