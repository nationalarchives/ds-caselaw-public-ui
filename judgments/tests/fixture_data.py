from caselawclient.factories import SearchResultFactory


class FakeSearchResponseBaseClass:
    """
    AbstractBaseClass for FakeSearchResponse, extend to
    modify attributes
    """

    total = 200
    results = [
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
        SearchResultFactory.build(),
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
