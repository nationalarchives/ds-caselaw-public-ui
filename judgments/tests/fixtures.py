from dataclasses import dataclass
from datetime import datetime


@dataclass
class FakeMetadata:
    author = "author"


@dataclass
class FakeSearchResult:
    uri = "ewhc/ch/2022/1"
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


class FakeSearchResponseBaseClass:
    """
    AbstractBaseClass for FakeSearchResponse, extend to
    modify attributes
    """

    total = 2
    results = [FakeSearchResult(), FakeSearchResult()]
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


class FakeSearchResponseNoFacets(FakeSearchResponseBaseClass):
    facets = {}
