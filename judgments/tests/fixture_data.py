from dataclasses import dataclass
from datetime import datetime


@dataclass
class FakeMetadata:
    author = "author"


@dataclass
class FakeSearchResult:
    uri = "d-123456789abcdef"
    neutral_citation = "neutral_citation"
    name = "A SearchResult name!"
    matches = None
    court = "court"
    date = datetime(2017, 8, 8, 0, 0)
    author = "author"
    last_modified = "last_modified"
    content_hash = "content_hash"
    transformation_date = "2023-04-09T18:05:45"
    metadata = FakeMetadata()
    slug = "fcl.x1y2z3"


class FakeSearchResponseBaseClass:
    """
    AbstractBaseClass for FakeSearchResponse, extend to
    modify attributes
    """

    total = 200
    results = [
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
        FakeSearchResult(),
    ]
    facets = {
        "EAT": "3",
        "EWHC-KBD-TCC": "1",
        " ": "5",
        "invalid_court": "10",
        "2010": "103",
        "1900": "4",
    }

    class Meta:
        abstract = True


class FakeSearchResponse(FakeSearchResponseBaseClass):
    pass


class FakeSearchResponseManyPages(FakeSearchResponseBaseClass):
    total = 999


class FakeSearchResponseNoFacets(FakeSearchResponseBaseClass):
    facets = {}


class FakeSearchResponseWithFacets(FakeSearchResponseBaseClass):
    total = 9999
    facets = {"2010": "9", "2011": "99", "EWCOP": "999", "": "1"}


class FakeSearchResponseNoResults(FakeSearchResponseBaseClass):
    total = 0
    results = []
