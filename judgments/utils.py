from datetime import datetime

from caselawclient.Client import api_client
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
):
    response = api_client.advanced_search(
        q=query,
        court=court,
        judge=judge,
        party=party,
        neutral_citation=neutral_citation,
        specific_keyword=specific_keyword,
        page=page,
        order=order,
        date_from=date_from,
        date_to=date_to,
    )
    multipart_data = decoder.MultipartDecoder.from_response(response)
    return SearchResults.create_from_string(multipart_data.parts[0].text)
