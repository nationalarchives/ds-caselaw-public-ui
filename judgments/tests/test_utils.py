import unittest
from unittest import mock

from caselawclient.errors import DocumentNotFoundError

from judgments.utils import get_document_by_uri
from judgments.views.detail import NoNeutralCitationError


class TestGetDocumentByUri(unittest.TestCase):
    @mock.patch("judgments.utils.MarklogicApiClient")
    def test_get_existing_document(self, mock_api_client):
        document = mock.Mock()
        mock_api_client.return_value.get_document_by_uri.return_value = document
        result = get_document_by_uri("sample_uri")
        self.assertEqual(result, document)

    @mock.patch("judgments.utils.MarklogicApiClient")
    def test_get_nonexistent_document(self, mock_api_client):
        mock_api_client.return_value.get_document_by_uri.side_effect = (
            DocumentNotFoundError
        )
        with self.assertRaises(DocumentNotFoundError):
            get_document_by_uri("nonexistent_uri")

    @mock.patch("judgments.utils.MarklogicApiClient")
    def test_get_document_not_judgment_or_press_summary(self, mock_api_client):
        document = mock.Mock()
        document.best_human_identifier = None
        mock_api_client.return_value.get_document_by_uri.return_value = document
        with self.assertRaises(NoNeutralCitationError):
            get_document_by_uri("nonexistent_uri")
