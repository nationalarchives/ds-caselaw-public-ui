from os import environ
from unittest.mock import patch

import pytest
from caselawclient.errors import JudgmentNotFoundError
from django.http import Http404, HttpResponseRedirect
from django.test import TestCase
from factories import JudgmentFactory

from judgments.views.detail import (
    PdfDetailView,
    get_pdf_size,
    get_published_judgment_by_uri,
)


class TestWeasyWithoutCSS(TestCase):
    @patch.object(PdfDetailView, "pdf_stylesheets", [])
    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_weasy_without_css_runs_in_ci(self, mock_judgment):
        judgment = JudgmentFactory.build(is_published=True)
        mock_judgment.return_value = judgment
        response = self.client.get("/eat/2023/1/generated.pdf")
        assert response.status_code == 200
        assert b"%PDF-1.7" in response.content


class TestGetPublishedJudgment:
    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_judgment_is_published(self, mock_judgment):
        judgment = JudgmentFactory.build(is_published=True)
        mock_judgment.return_value = judgment
        assert get_published_judgment_by_uri("2022/eat/1") == judgment

    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_judgment_is_unpublished(self, mock_judgment):
        mock_judgment.return_value = JudgmentFactory.build(is_published=False)
        with pytest.raises(Http404):
            get_published_judgment_by_uri("2099/eat/1")

    @patch(
        "judgments.views.detail.get_judgment_by_uri", side_effect=JudgmentNotFoundError
    )
    def test_judgment_missing(self, mock_judgment):
        with pytest.raises(Http404):
            get_published_judgment_by_uri("not-a-judgment")

    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_press_summary_is_published(self, mock_judgment):
        judgment = JudgmentFactory.build(
            is_published=True, uri="2022/eat/1/press-summary/1"
        )
        mock_judgment.return_value = judgment
        assert get_published_judgment_by_uri("2022/eat/1/press-summary/1") == judgment


class TestJudgment(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_judgment_by_uri")
    def test_published_judgment_response(self, mock_judgment, mock_pdf_size):
        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = "1234KB"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

        self.assertIn("<p>This is a judgment in HTML.</p>", decoded_response)
        self.assertIn(
            '<meta name="robots" content="noindex,nofollow" />', decoded_response
        )

        self.assertEqual(response.status_code, 200)


class TestJudgmentBackToSearchLink(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_judgment_by_uri")
    def test_no_link_if_no_context(self, mock_judgment, mock_pdf_size):
        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = "1234KB"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        assert "Back to search results" not in decoded_response


class TestJudgmentPdfLinkText(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_judgment_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_size(self, mock_judgment, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns a non-empty string (either a file size or
        "unknown"), in which case we should link to the file in S3 via our assets URL and display the size string.
        """

        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = " (1234KB)"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertIn(
            "https://example.com/test/2023/123/test_2023_123.pdf", decoded_response
        )
        self.assertNotIn("data.pdf", decoded_response)
        self.assertIn("(1234KB)", decoded_response)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_judgment_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_no_size(self, mock_judgment, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns an empty string (implying that the file doesn't
        exist in S3), so we should link to our generated PDF instead and not S3."""

        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = ""

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertNotIn("test_2023_123.pdf", decoded_response)
        self.assertIn("/test/2023/123/data.pdf", decoded_response)


class TestGetPdfSize(TestCase):
    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_returns_valid_size(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {"Content-Length": "1234567890"}
        mock_head.return_value.status_code = 200
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == " (1.1\xa0GB)"
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )

    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_pdf_exists_with_no_size(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {}
        mock_head.return_value.status_code = 200
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == " (unknown size)"
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )

    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_no_pdf_exists(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {}
        mock_head.return_value.status_code = 404
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == ""
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )


class TestDocumentURIRedirects(TestCase):
    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_non_canonical_uri_redirects(self, mock_judgment):
        mock_judgment.return_value = JudgmentFactory.build(
            uri="test/1234/567", is_published=True
        )
        response = self.client.get("/test/1234/567/")
        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == "/test/1234/567"
