from unittest.mock import Mock, patch

import pytest
from caselawclient.errors import DocumentNotFoundError, MarklogicNotPermittedError
from caselawclient.factories import JudgmentFactory
from caselawclient.models.documents import DocumentURIString
from django.http import Http404
from django.test import TestCase

from judgments.utils import (
    get_published_document_by_uri,
)


class TestGetPublishedDocument(TestCase):
    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_judgment_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True)
        mock_get_document_by_uri.return_value = judgment
        document_uri = DocumentURIString("2022/eat/1")
        assert get_published_document_by_uri(document_uri) == judgment

    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_judgment_is_unpublished(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=False)
        with pytest.raises(Http404):
            document_uri = DocumentURIString("2099/eat/1")
            get_published_document_by_uri(document_uri)

    @patch("judgments.utils.judgment_utils.get_document_by_uri", side_effect=DocumentNotFoundError)
    def test_judgment_missing(self, mock_get_document_by_uri):
        with pytest.raises(Http404):
            document_uri = DocumentURIString("not-a-judgment")
            get_published_document_by_uri(document_uri)

    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_press_summary_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True, uri=DocumentURIString("2022/eat/1/press-summary/1"))
        mock_get_document_by_uri.return_value = judgment
        document_uri = DocumentURIString("2022/eat/1/press-summary/1")
        assert get_published_document_by_uri(document_uri) == judgment

    @patch("judgments.utils.judgment_utils.get_document_by_uri", return_value=None)
    def test_raises_404_if_document_is_none(self, mock_get):
        document_uri = DocumentURIString("2022/eat/1")

        with self.assertRaises(Http404) as ctx:
            get_published_document_by_uri(document_uri)
        assert "was not found" in str(ctx.exception)

    @patch("judgments.utils.judgment_utils.get_document_by_uri", side_effect=DocumentNotFoundError)
    def test_raises_404_on_document_not_found_error(self, mock_get):
        document_uri = DocumentURIString("2022/eat/1")
        with self.assertRaises(Http404) as ctx:
            get_published_document_by_uri(document_uri)
        assert "was not found" in str(ctx.exception)

    @patch("judgments.utils.judgment_utils.get_document_by_uri", side_effect=MarklogicNotPermittedError)
    def test_raises_404_on_marklogic_not_permitted_error(self, mock_get):
        document_uri = DocumentURIString("2022/eat/1")
        with self.assertRaises(Http404) as ctx:
            get_published_document_by_uri(document_uri)
        assert "is not available" in str(ctx.exception)

    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_raises_404_if_document_not_published(self, mock_get):
        mock_doc = Mock()
        mock_doc.is_published = False
        mock_get.return_value = mock_doc

        document_uri = DocumentURIString("2022/eat/1")
        with self.assertRaises(Http404) as ctx:
            get_published_document_by_uri(document_uri)
        assert "is not available" in str(ctx.exception)
