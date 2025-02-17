from dataclasses import dataclass
from datetime import datetime
from unittest.mock import patch

import pytest
from caselawclient.factories import IdentifierResolutionFactory, IdentifierResolutionsFactory
from django.test import TestCase

from judgments.resolvers.document_resolver_engine import api_client


def _echo_resolution(url):
    assert "ml-" not in url
    return IdentifierResolutionsFactory.build(
        [IdentifierResolutionFactory.build(identifier_slug=url, document_uri=f"/ml-{url}.xml")]
    )


class TestCaseWithMockAPI(TestCase):
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        with patch.object(
            api_client,
            "resolve_from_identifier_slug",
            side_effect=_echo_resolution,
        ):
            yield


class TestCaseWithNoResolutions(TestCase):
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        with patch.object(
            api_client, "resolve_from_identifier_slug", return_value=IdentifierResolutionsFactory.build([])
        ):
            yield


class TestCaseWithMultipleResolutions(TestCase):
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        with patch.object(
            api_client,
            "resolve_from_identifier_slug",
            return_value=IdentifierResolutionsFactory.build(
                [
                    IdentifierResolutionFactory.build(identifier_slug="x", document_uri="/ml-x-1.xml"),
                    IdentifierResolutionFactory.build(identifier_slug="x", document_uri="/ml-x-2.xml"),
                ]
            ),
        ):
            yield


@pytest.mark.django_db
class MockAPI:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        with patch.object(
            api_client,
            "resolve_from_identifier_slug",
            side_effect=_echo_resolution,
        ):
            yield


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
