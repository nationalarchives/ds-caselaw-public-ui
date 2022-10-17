import re
from datetime import datetime

from caselawclient.Client import RESULTS_PER_PAGE, api_client
from requests_toolbelt.multipart import decoder

from .models import SearchResults


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


def remove_unquoted_stop_words(query):
    """
    Remove stop words [the, and, of] from a search query, but only if they
    are part of an unquoted string AND are not the only word.
    If they are part of a quoted string, e.g.
    'body of evidence', or are the only word, they are left alone.
    """
    if (
        re.match(r"^\"|^\'", query) is None
        and re.match(r"\"$|\'$", query) is None
        and re.match(r"(^the$)|(^of$)|(^and$)", query) is None
    ):
        without_stop_words = re.sub(
            r"(\band\b)|(\bof\b)|(\bthe\b)", "", query, re.IGNORECASE
        )
        return re.sub(r"\s+", " ", without_stop_words)
    return query
