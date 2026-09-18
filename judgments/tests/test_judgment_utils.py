from datetime import datetime
from unittest.mock import Mock, patch
from urllib.parse import quote

from caselawclient.models.documents import DocumentURIString
from django.test import TestCase

from judgments.utils import get_document_download_filename, get_judgement_date


class TestGetDocumentDownloadFilename(TestCase):
    example_uri = DocumentURIString("case/2025/1234")

    @patch("judgments.utils.judgment_utils.get_published_document_by_uri")
    def test_returns_combined_filename_if_all_present(self, mock_get_document_by_uri):
        mock_document = Mock()
        mock_document.body.name = "Smith-v-Jones"
        mock_document.best_human_identifier.value = "2025-EWHC-12"
        mock_get_document_by_uri.return_value = mock_document

        result = get_document_download_filename(self.example_uri)
        expected = quote("Smith-v-Jones-2025-EWHC-12")
        assert result == expected

    @patch("judgments.utils.judgment_utils.get_published_document_by_uri")
    def test_returns_document_name_if_only_body_present(self, mock_get_document_by_uri):
        mock_document = Mock()
        mock_document.body.name = "Smith-v-Jones"
        mock_document.best_human_identifier = None
        mock_get_document_by_uri.return_value = mock_document

        result = get_document_download_filename(self.example_uri)
        expected = quote("Smith-v-Jones")
        assert result == expected

    @patch("judgments.utils.judgment_utils.get_published_document_by_uri")
    def test_returns_quoted_uri_if_document_is_none(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = None

        result = get_document_download_filename(self.example_uri)
        assert result == quote(self.example_uri)

    @patch("judgments.utils.judgment_utils.get_published_document_by_uri")
    def test_uses_supplied_document_without_fetching_again(self, mock_get_document_by_uri):
        mock_document = Mock()
        mock_document.body.name = "Smith-v-Jones"
        mock_document.best_human_identifier.value = "2025-EWHC-12"

        result = get_document_download_filename(self.example_uri, mock_document)
        expected = quote("Smith-v-Jones-2025-EWHC-12")
        assert result == expected
        mock_get_document_by_uri.assert_not_called()


class TestGetJudgementDate(TestCase):
    def test_returns_none_without_a_date(self):
        result = Mock()
        result.node.xpath.return_value = []

        assert get_judgement_date(result) is None
        result.date.assert_not_called()

    def test_uses_the_client_date_for_a_real_date(self):
        result = Mock()
        result.node.xpath.return_value = ["2023-02-03"]
        result.date = datetime(2023, 2, 3)  # noqa: DTZ001

        assert get_judgement_date(result) == datetime(2023, 2, 3)  # noqa: DTZ001
