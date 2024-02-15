import unittest
from unittest import mock

from caselawclient.errors import DocumentNotFoundError

from judgments.utils import formatted_document_uri, get_document_by_uri


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

    def test_formatted_document_uri(self):
        test_params = [
            ("pdf", "/data.pdf"),
            ("generated_pdf", "/generated.pdf"),
            ("xml", "/data.xml"),
            ("html", "/data.html"),
        ]
        document_uri = "ewhc/comm/2024/253"
        for format, suffix in test_params:
            with self.subTest(format=format, suffix=suffix):
                self.assertEqual(
                    formatted_document_uri(document_uri, format),
                    "/" + document_uri + suffix,
                )
