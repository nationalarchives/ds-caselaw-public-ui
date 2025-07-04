from unittest.mock import Mock, patch
from urllib.parse import quote

from caselawclient.models.documents import DocumentURIString
from django.test import TestCase

from judgments.utils import get_document_download_filename


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
    def test_returns_quoted_uri_if_document_is_none(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = None

        result = get_document_download_filename(self.example_uri)
        assert result == quote(self.example_uri)
