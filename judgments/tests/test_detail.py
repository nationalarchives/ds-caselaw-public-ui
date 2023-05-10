from os import environ
from unittest.mock import patch

import pytest
from caselawclient.errors import JudgmentNotFoundError
from django.http import Http404
from django.test import TestCase
from django.urls.exceptions import Resolver404
from factories import JudgmentFactory

from judgments.views.detail import get_pdf_size, get_published_judgment_by_uri


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

    def test_judgment_url_with_trailing_stuff_fails_to_resolve(self, client):
        response = client.get("/eat/2022/1/kitten")
        with pytest.raises(Resolver404):
            response.resolver_match.func


class TestJudgment(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_judgment_by_uri")
    def test_published_judgment_response(self, mock_judgment, mock_pdf_size):
        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = "1234KB"

        response = self.client.get("/eat/1234/123")
        decoded_response = response.content.decode("utf-8")

        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

        self.assertIn("<p>This is a judgment in HTML.</p>", decoded_response)
        self.assertIn(
            '<meta name="robots" content="noindex,nofollow" />', decoded_response
        )

        self.assertEqual(response.status_code, 200)


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

        response = self.client.get("/eat/1234/123")
        decoded_response = response.content.decode("utf-8")

        self.assertIn(
            "https://example.com/eat/ch/2099/123/eat_ch_2099_123.pdf", decoded_response
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

        response = self.client.get("/eat/1234/123")
        decoded_response = response.content.decode("utf-8")

        self.assertNotIn("123.pdf", decoded_response)
        self.assertIn("/eat/ch/2099/123/data.pdf", decoded_response)


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
