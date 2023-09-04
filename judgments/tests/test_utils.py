import unittest
from unittest import mock

from caselawclient.errors import DocumentNotFoundError

from judgments.utils import get_document_by_uri


class TestGetDocumentByUri(unittest.TestCase):
    @mock.patch("judgments.utils.api_client")
    def test_get_existing_document(self, mock_api_client):
        document = mock.Mock()
        mock_api_client.get_document_by_uri.return_value = document
        result = get_document_by_uri("sample_uri")
        self.assertEqual(result, document)

    @mock.patch("judgments.utils.api_client")
    def test_get_nonexistent_document(self, mock_api_client):
        mock_api_client.get_document_by_uri.side_effect = DocumentNotFoundError
        with self.assertRaises(DocumentNotFoundError):
            get_document_by_uri("nonexistent_uri")
