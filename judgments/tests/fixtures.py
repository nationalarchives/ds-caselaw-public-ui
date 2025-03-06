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
