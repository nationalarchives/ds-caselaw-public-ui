import math
import re
from functools import lru_cache
from time import time
from typing import Any, Literal, Optional, TypedDict, overload
from urllib.parse import parse_qs, urlparse

from caselawclient.Client import DEFAULT_USER_AGENT, MarklogicApiClient
from caselawclient.errors import DocumentNotFoundError
from caselawclient.models.documents import Document, DocumentURIString
from caselawclient.models.press_summaries import PressSummary
from caselawclient.search_parameters import RESULTS_PER_PAGE
from django.conf import settings
from django.urls import reverse
from ds_caselaw_utils.neutral import neutral_url
from ds_caselaw_utils.types import NeutralCitationString

from judgments.fixtures.stop_words import stop_words

MAX_RESULTS_PER_PAGE = 50

api_client = MarklogicApiClient(
    host=settings.MARKLOGIC_HOST,
    username=settings.MARKLOGIC_USER,
    password=settings.MARKLOGIC_PASSWORD,
    use_https=settings.MARKLOGIC_USE_HTTPS,
    user_agent=f"ds-caselaw-public-ui/unknown {DEFAULT_USER_AGENT}",
)


def format_date(date):
    if date == "" or date is None:
        return None

    time = date.strptime(date, "%Y-%m-%d")
    return time.strftime("%d-%m-%Y")


def preprocess_query(query: str) -> str:
    query = normalise_quotes(query)
    query = normalise_spaces(query)
    query = normalise_vs(query)
    query = remove_unquoted_stop_words(query)
    return query


def normalise_vs(query):
    # Note: this assumes it runs after spaces are normalised
    return re.sub(r"-? ?\bvs?\b ?-?", " v ", query, re.IGNORECASE)


def normalise_spaces(query):
    return re.sub(" +", " ", query)


def normalise_quotes(query):
    return re.sub(r"[“”]", '"', query)


def remove_unquoted_stop_words(query):
    """
    Remove stop words [the, and, of] from a search query, but only if they
    are part of an unquoted string AND are not the only word.
    If they are part of a quoted string, e.g.
    'body of evidence', or are the only word, they are left alone.
    """
    if query is None:
        return
    if (
        re.match(r"^\"|^\'", query) is None
        and re.match(r"\"$|\'$", query) is None
        and re.match(solo_stop_word_regex(stop_words), query) is None
    ):
        without_stop_words = re.sub(without_stop_words_regex(stop_words), "", query, re.IGNORECASE)
        return re.sub(r"\s+", " ", without_stop_words)
    return query


def without_stop_words_regex(stops):
    modified_stops = [f"(\\b{stop}\\b)" for stop in stops]
    regex = r"|".join(modified_stops)
    return regex


def solo_stop_word_regex(stops):
    modified_stops = [f"(^{stop}$)" for stop in stops]
    regex = r"|".join(modified_stops)
    return regex


def sanitise_input_to_integer(input: Any, default: int) -> int:
    try:
        return int(input)
    except (ValueError, TypeError):
        return default


def clamp(
    number: int,
    minimum: int,
    maximum: Optional[int] = None,
) -> int:
    """
    Clamp an integer, making sure it's between the min and max
    """

    min_bounded = max(minimum, number)
    if maximum is not None:
        return min(min_bounded, maximum)
    else:
        return min_bounded


def paginator(current_page: int, total, size_per_page: int = RESULTS_PER_PAGE):
    number_of_pagination_links = 5
    current_page = clamp(current_page, minimum=1)
    size_per_page = clamp(
        size_per_page,
        minimum=1,
        maximum=MAX_RESULTS_PER_PAGE,
    )
    number_of_pages = math.ceil(int(total) / size_per_page)

    half_range = number_of_pagination_links // 2

    if number_of_pages <= number_of_pagination_links:
        page_range = list(range(1, number_of_pages + 1))
    elif current_page - half_range < 1:
        page_range = list(range(1, number_of_pagination_links + 1))
    elif current_page + half_range > number_of_pages:
        page_range = list(range(number_of_pages - number_of_pagination_links + 1, number_of_pages + 1))
    else:
        page_range = list(range(current_page - half_range, current_page + half_range + 1))

    show_first_page = 1 not in page_range
    show_first_page_divider = number_of_pages > number_of_pagination_links and 2 not in page_range
    show_last_page = number_of_pages not in page_range
    show_last_page_divider = number_of_pages > number_of_pagination_links and number_of_pages - 1 not in page_range

    return {
        "show_first_page": show_first_page,
        "show_first_page_divider": show_first_page_divider,
        "show_last_page": show_last_page,
        "show_last_page_divider": show_last_page_divider,
        "current_page": current_page,
        "has_next_page": current_page < number_of_pages,
        "next_page": current_page + 1,
        "has_prev_page": current_page > 1,
        "prev_page": current_page - 1,
        "number_of_pages": number_of_pages,
        "page_range": page_range,
    }


class SearchContextDict(TypedDict):
    search_url: str
    query: Optional[str]


def search_context_from_url(url) -> Optional[dict]:
    """
    We only display the 'back' link on a judgment detail page if the user
    navigated from a search result page. This method determines if the referrer
    corresponds to a search result page, and conditionally returns the link if so.
    """
    if url:
        parsed_url = urlparse(url)
        is_search_link = parsed_url.path in [
            "/judgments/results",
            "/judgments/advanced_search",
            "/judgments/search",
        ]

        if is_search_link:
            query_elements = parse_qs(parsed_url.query).get("query", None)
            query = query_elements[0] if query_elements else None

            return {
                "search_url": url,
                "query": query,
            }
    return None


def has_filters(query_params, exclude=["order", "per_page"]):
    """
    This method returns true if the query parameters contain any filters,
    be they query string, court, date, or party.
    """
    return len(set(k for (k, v) in query_params.items() if v) - set(exclude)) > 0


@overload
def get_document_by_uri(
    document_uri: str, max_ttl: int = 900, cache_if_not_found: Literal[False] = False
) -> Document: ...


@overload
def get_document_by_uri(
    document_uri: str, max_ttl: int = 900, cache_if_not_found: bool = False
) -> Optional[Document]: ...


def get_document_by_uri(document_uri: str, max_ttl: int = 900, cache_if_not_found: bool = False) -> Optional[Document]:
    """
    This is a wrapper for getting a document from the cache, with a maximum TTL. The `max_ttl` is a [workaround](https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live) for the fact `lru_cache` doesn't have any time-based expiry
    """
    ttl_hash = round(time() / max_ttl)
    return get_document_by_uri_from_cache(
        DocumentURIString(document_uri), ttl_hash=ttl_hash, cache_if_not_found=cache_if_not_found
    )


@lru_cache(maxsize=256)
def get_document_by_uri_from_cache(
    document_uri: DocumentURIString, ttl_hash: int = 0, cache_if_not_found: bool = False
) -> Optional[Document]:
    del ttl_hash  # ttl_hash is used to fake cache expiry with time

    # Try to get the document. If it doesn't exist and `cache_if_not_found` is `True`, return a `None` response so it will be cached. Otherwise, bubble the exception up.
    try:
        return api_client.get_document_by_uri(document_uri)
    except DocumentNotFoundError as e:
        if cache_if_not_found:
            return None
        raise e


def get_press_summaries_for_document_uri(document_uri: str) -> list[PressSummary]:
    return api_client.get_press_summaries_for_document_uri(DocumentURIString(document_uri))


def formatted_document_uri(document_uri: DocumentURIString, format: Optional[str] = None) -> str:
    url = reverse("detail", args=[document_uri])
    if format == "pdf":
        url = url + "/data.pdf"
    elif format == "generated_pdf":
        url = url + "/generated.pdf"
    elif format == "xml":
        url = url + "/data.xml"
    elif format == "html":
        url = url + "/data.html"

    return url


def linked_doc_url(document: Document) -> DocumentURIString:
    press_summary_suffix = "/press-summary/1"
    if document.document_noun == "press summary":
        return DocumentURIString(document.uri.removesuffix(press_summary_suffix))
    else:
        return DocumentURIString(document.uri + press_summary_suffix)


def linked_doc_title(document: Document):
    press_summary_title_prefix = "Press Summary of "
    if document.document_noun == "press summary":
        return document.body.name.removeprefix(press_summary_title_prefix)
    else:
        return press_summary_title_prefix + document.body.name


def press_summary_list_breadcrumbs(press_summary: Document):
    return [
        {
            "url": "/" + linked_doc_url(press_summary),
            "text": linked_doc_title(press_summary),
        },
        {
            "text": "Press Summaries",
        },
    ]


not_alphanumeric = re.compile("[^a-zA-Z0-9]")


def replace_parens(string: str) -> str:
    return normalise_spaces(re.sub("\\(.+\\)", "", string))


def preprocess_title(string: str) -> str:
    return preprocess_query(replace_parens(string)).lower().strip()


def preprocess_ncn(string: str) -> str:
    return re.sub(not_alphanumeric, "", preprocess_query(string).lower()).strip()


def is_exact_ncn_match(result, query: str) -> bool:
    return preprocess_ncn(query) == preprocess_ncn(result.neutral_citation)


def search_results_have_exact_ncn(search_results, query: str) -> bool:
    for search_result in search_results:
        if is_exact_ncn_match(search_result, query):
            return True
    return False


def show_no_exact_ncn_warning(search_results, query_text: str, page: int) -> bool:
    return (
        not (search_results_have_exact_ncn(search_results, query_text))
        and bool(
            neutral_url(NeutralCitationString(query_text))
        )  ## TODO: This is horrible, because we don't know query_text is a valid NCN at this point
        and page == 1
    )
