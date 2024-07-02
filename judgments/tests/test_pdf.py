from os import environ
from unittest.mock import Mock, patch

from judgments.models.document_pdf import DocumentPdf
from judgments.tests.factories import JudgmentFactory
from judgments.utils import formatted_document_uri


class TestDocumentPdf:
    @patch("judgments.models.document_pdf.requests")
    def test_get_pdf_size_returns_pdf_size_if_it_exists(self, requests_mock):
        content_length = "100"
        head_mock = Mock(headers={"Content-Length": content_length}, status_code=200)
        requests_mock.head.return_value = head_mock

        document = JudgmentFactory.build()
        document_pdf = DocumentPdf(document.uri)

        assert document_pdf.size == 100

        requests_mock.head.assert_called_once_with(document_pdf.generate_uri(), headers={"Accept-Encoding": None})

    @patch("judgments.models.document_pdf.requests")
    def test_get_pdf_size_returns_blank_string_if_404(self, requests_mock):
        head_mock = Mock(status_code=404)
        requests_mock.head.return_value = head_mock

        document = JudgmentFactory.build()
        document_pdf = DocumentPdf(document.uri)

        assert document_pdf.size is None

    @patch("judgments.models.document_pdf.requests")
    def test_get_pdf_size_returns_unknown_when_no_content_size(self, requests_mock):
        head_mock = Mock(headers={}, status_code=200)
        requests_mock.head.return_value = head_mock

        document = JudgmentFactory.build()
        document_pdf = DocumentPdf(document.uri)

        assert document_pdf.size is None

    def test_returns_pdf_uri_if_exists(self):
        document = JudgmentFactory.build()
        document_pdf = DocumentPdf(document.uri)
        document_pdf.size = 100

        assert document_pdf.uri == document_pdf.generate_uri()

    def test_generates_uri_if_does_not_exist(self):
        document = JudgmentFactory.build()
        document_pdf = DocumentPdf(document.uri)
        document_pdf.size = None

        assert document_pdf.uri == formatted_document_uri(document.uri, "pdf")

    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.org"})
    def generate_uri_generates_the_correct_uri_with_base_url(self):
        document_pdf = DocumentPdf("foo/bar/baz")

        assert document_pdf.generate_uri() == "https://example.org/foo_bar_baz.pdf"

    @patch.dict(
        environ,
        {
            "ASSETS_CDN_BASE_URL": "",
            "PUBLIC_ASSET_BUCKET": "bucket",
            "S3_REGION": "region",
        },
    )
    def test_generate_uri_generates_the_correct_uri_with_base_url(self):
        document_pdf = DocumentPdf("foo/bar/baz")

        assert document_pdf.generate_uri() == "https://bucket.s3.region.amazonaws.com/foo/bar/baz/foo_bar_baz.pdf"
