from unittest.mock import patch

import pytest
from caselawclient.errors import DocumentNotFoundError
from caselawclient.factories import JudgmentFactory
from caselawclient.models.documents import DocumentURIString
from django.http import Http404

from judgments.utils import (
    get_published_document_by_uri,
)


class TestGetPublishedDocument:
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
