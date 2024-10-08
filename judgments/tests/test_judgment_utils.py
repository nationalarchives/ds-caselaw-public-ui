from unittest.mock import patch

import pytest
from caselawclient.errors import DocumentNotFoundError
from django.http import Http404
from factories import JudgmentFactory

from judgments.utils import (
    get_published_document_by_uri,
)


class TestGetPublishedDocument:
    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_judgment_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True)
        mock_get_document_by_uri.return_value = judgment
        assert get_published_document_by_uri("2022/eat/1") == judgment

    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_judgment_is_unpublished(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=False)
        with pytest.raises(Http404):
            get_published_document_by_uri("2099/eat/1")

    @patch("judgments.utils.judgment_utils.get_document_by_uri", side_effect=DocumentNotFoundError)
    def test_judgment_missing(self, mock_get_document_by_uri):
        with pytest.raises(Http404):
            get_published_document_by_uri("not-a-judgment")

    @patch("judgments.utils.judgment_utils.get_document_by_uri")
    def test_press_summary_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True, uri="2022/eat/1/press-summary/1")
        mock_get_document_by_uri.return_value = judgment
        assert get_published_document_by_uri("2022/eat/1/press-summary/1") == judgment
