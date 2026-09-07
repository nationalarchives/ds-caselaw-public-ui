from unittest.mock import Mock, patch

import requests
from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase
from django.urls import reverse

from judgments.models.document_pdf import DocumentPdf
from judgments.views.detail import best_pdf
from judgments.views.detail.best_pdf import PDF_STREAM_CHUNK_SIZE


class BestPdfViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.document_uri = "test/2025/123"
        self.mock_pdf_uri = "http://mock-s3-url.com/example-document.pdf"

    @patch("judgments.views.detail.best_pdf.get_document_download_filename")
    @patch.object(DocumentPdf, "generate_uri")
    @patch("requests.get")
    def test_returns_pdf_when_found(self, mock_get, mock_generate_uri, mock_get_filename):
        mock_generate_uri.return_value = self.mock_pdf_uri
        mock_get.return_value = Mock(status_code=200, iter_content=Mock(return_value=[b"%PDF-1.4 ", b"binary data"]))
        mock_get_filename.return_value = "some_download_filename"

        request = self.factory.get(f"/data/{self.document_uri}.pdf")
        response = best_pdf(request, self.document_uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            "attachment; filename=\"some_download_filename.pdf\"; filename*=UTF-8''some_download_filename.pdf",
        )
        self.assertIn(b"%PDF-1.4", b"".join(response.streaming_content))
        mock_get.assert_called_once_with(self.mock_pdf_uri, stream=True, timeout=10)
        mock_get.return_value.iter_content.assert_called_once_with(chunk_size=PDF_STREAM_CHUNK_SIZE)
        mock_get.return_value.close.assert_called_once()

    @patch.object(DocumentPdf, "generate_uri")
    @patch("requests.get")
    def test_redirects_to_weasyprint_when_not_found(self, mock_get, mock_generate_uri):
        mock_generate_uri.return_value = self.mock_pdf_uri
        mock_get.return_value = Mock(status_code=404)

        request = self.factory.get(f"/data/{self.document_uri}.pdf")
        response = best_pdf(request, self.document_uri)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(
            response.url,
            reverse(
                "detail",
                kwargs={"document_uri": self.document_uri, "file_format": "generated.pdf"},
            ),
        )

    @patch.object(DocumentPdf, "generate_uri")
    @patch("requests.get")
    def test_logs_warning_and_redirects_on_unexpected_error(self, mock_get, mock_generate_uri):
        mock_generate_uri.return_value = self.mock_pdf_uri
        mock_get.return_value = Mock(status_code=500)

        with self.assertLogs(level="WARNING") as log:
            request = self.factory.get(f"/data/{self.document_uri}.pdf")
            response = best_pdf(request, self.document_uri)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn(f"Unexpected 500 error on {self.document_uri}", log.output[0])

    @patch.object(DocumentPdf, "generate_uri")
    @patch("requests.get")
    def test_logs_warning_and_redirects_on_request_failure(self, mock_get, mock_generate_uri):
        mock_generate_uri.return_value = self.mock_pdf_uri
        mock_get.side_effect = requests.exceptions.ConnectionError

        with self.assertLogs(level="WARNING") as log:
            request = self.factory.get(f"/data/{self.document_uri}.pdf")
            response = best_pdf(request, self.document_uri)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(
            response.url,
            reverse(
                "detail",
                kwargs={"document_uri": self.document_uri, "file_format": "generated.pdf"},
            ),
        )
        self.assertIn(f"Request failed trying to get best_pdf for {self.document_uri}", log.output[0])

    @patch.object(DocumentPdf, "generate_uri")
    @patch("requests.get")
    def test_logs_warning_and_redirects_on_request_timeout(self, mock_get, mock_generate_uri):
        mock_generate_uri.return_value = self.mock_pdf_uri
        mock_get.side_effect = requests.exceptions.Timeout

        with self.assertLogs(level="WARNING") as log:
            request = self.factory.get(f"/data/{self.document_uri}.pdf")
            response = best_pdf(request, self.document_uri)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(
            response.url,
            reverse(
                "detail",
                kwargs={"document_uri": self.document_uri, "file_format": "generated.pdf"},
            ),
        )
        self.assertIn(f"Timed out trying to get best_pdf for {self.document_uri}", log.output[0])
