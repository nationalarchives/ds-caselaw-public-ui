import math
import re
from datetime import datetime
from urllib.parse import urlparse

import environ
from caselawclient.Client import RESULTS_PER_PAGE, api_client
from requests_toolbelt.multipart import decoder

from .fixtures.stop_words import stop_words
from .models import SearchResults

MAX_RESULTS_PER_PAGE = 50


def format_date(date):
    if date == "" or date is None:
        return None

    time = datetime.strptime(date, "%Y-%m-%d")
    return time.strftime("%d-%m-%Y")


def perform_advanced_search(
    query=None,
    court=None,
    judge=None,
    party=None,
    order=None,
    neutral_citation=None,
    specific_keyword=None,
    date_from=None,
    date_to=None,
    page=1,
    per_page=RESULTS_PER_PAGE,
):
    response = api_client.advanced_search(
        q=query,
        court=",".join(court) if isinstance(court, list) else court,
        judge=judge,
        party=party,
        neutral_citation=neutral_citation,
        specific_keyword=specific_keyword,
        page=page,
        order=order,
        date_from=date_from,
        date_to=date_to,
        page_size=per_page,
    )
    multipart_data = decoder.MultipartDecoder.from_response(response)
    return SearchResults.create_from_string(multipart_data.parts[0].text)


def preprocess_query(query):
    query = normalise_quotes(query)
    query = remove_unquoted_stop_words(query)
    return query


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
        without_stop_words = re.sub(
            without_stop_words_regex(stop_words), "", query, re.IGNORECASE
        )
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


def as_integer(number_string, minimum, maximum=None, default=None):
    """
    Return an integer for user input, making sure it's between the min and max,
    and if it's not a valid number, that it's the default (or minimum if not set).
    """

    if default is None:
        default = minimum
    if number_string is None:
        return default
    try:
        number = int(number_string)
    except ValueError:
        return default

    min_bounded = max(minimum, number)
    if maximum is not None:
        return min(min_bounded, maximum)
    else:
        return min_bounded


def paginator(current_page, total, size_per_page=RESULTS_PER_PAGE):
    current_page = as_integer(current_page, minimum=1)
    size_per_page = as_integer(
        size_per_page, minimum=1, maximum=MAX_RESULTS_PER_PAGE, default=RESULTS_PER_PAGE
    )
    number_of_pages = math.ceil(int(total) / size_per_page)
    next_pages = list(
        range(current_page + 1, min(current_page + 10, number_of_pages) + 1)
    )

    return {
        "current_page": current_page,
        "has_next_page": current_page < number_of_pages,
        "next_page": current_page + 1,
        "has_prev_page": current_page > 1,
        "prev_page": current_page - 1,
        "next_pages": next_pages,
        "number_of_pages": number_of_pages,
    }


def get_pdf_uri(judgment_uri):
    env = environ.Env()
    """Create a string saying where the S3 PDF will be for a judgment uri"""
    pdf_path = f'{judgment_uri}/{judgment_uri.replace("/", "_")}.pdf'
    assets = env("ASSETS_CDN_BASE_URL", default=None)
    if assets:
        return f"{assets}/{pdf_path}"
    else:
        return f'https://{env("PUBLIC_ASSET_BUCKET")}.s3.{env("S3_REGION")}.amazonaws.com/{pdf_path}'


def display_back_link(back_link):
    """
    We only display the 'back' link on a judgment detail page if the user
    navigated from a search result page. This method determines if the referrer
    corresponds to a search result page, and conditionally returns the link if so.
    """
    if back_link:
        url = urlparse(back_link)
        return url.path in ["/judgments/results", "/judgments/advanced_search"]
    else:
        return False


def has_filters(query_params, exclude=["order", "per_page"]):
    """
    This method returns true if the query parameters contain any filters,
    be they query string, court, date, or party.
    """
    return len(set(k for (k, v) in query_params.items() if v) - set(exclude)) > 0
