from os import environ
from unittest.mock import patch

import pytest
from caselawclient.errors import JudgmentNotFoundError
from django.http import Http404, HttpResponseRedirect
from django.test import Client, TestCase
from factories import JudgmentFactory

from judgments.tests.utils.assertions import (
    assert_contains_html,
    assert_not_contains_html,
)
from judgments.views.detail import (
    PdfDetailView,
    get_pdf_size,
    get_published_document_by_uri,
)


class TestWeasyWithoutCSS(TestCase):
    @patch.object(PdfDetailView, "pdf_stylesheets", [])
    @patch("judgments.views.detail.get_document_by_uri")
    def test_weasy_without_css_runs_in_ci(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True)
        mock_get_document_by_uri.return_value = judgment
        response = self.client.get("/eat/2023/1/generated.pdf")
        assert response.status_code == 200
        assert b"%PDF-1.7" in response.content


class TestGetPublishedDocument:
    @patch("judgments.views.detail.get_document_by_uri")
    def test_judgment_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(is_published=True)
        mock_get_document_by_uri.return_value = judgment
        assert get_published_document_by_uri("2022/eat/1") == judgment

    @patch("judgments.views.detail.get_document_by_uri")
    def test_judgment_is_unpublished(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=False
        )
        with pytest.raises(Http404):
            get_published_document_by_uri("2099/eat/1")

    @patch(
        "judgments.views.detail.get_document_by_uri", side_effect=JudgmentNotFoundError
    )
    def test_judgment_missing(self, mock_get_document_by_uri):
        with pytest.raises(Http404):
            get_published_document_by_uri("not-a-judgment")

    @patch("judgments.views.detail.get_document_by_uri")
    def test_press_summary_is_published(self, mock_get_document_by_uri):
        judgment = JudgmentFactory.build(
            is_published=True, uri="2022/eat/1/press-summary/1"
        )
        mock_get_document_by_uri.return_value = judgment
        assert get_published_document_by_uri("2022/eat/1/press-summary/1") == judgment


class TestJudgment(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_document_by_uri")
    def test_published_judgment_response(self, mock_get_document_by_uri, mock_pdf_size):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
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
    @patch("judgments.views.detail.get_published_document_by_uri")
    def test_no_link_if_no_context(self, mock_get_document_by_uri, mock_pdf_size):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = "1234KB"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        assert "Back to search results" not in decoded_response


class TestJudgmentPdfLinkText(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_document_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_size(self, mock_get_document_by_uri, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns a non-empty string (either a file size or
        "unknown"), in which case we should link to the file in S3 via our assets URL and display the size string.
        """

        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = " (1234KB)"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertIn(
            "https://example.com/test/2023/123/test_2023_123.pdf", decoded_response
        )
        self.assertNotIn("data.pdf", decoded_response)
        self.assertIn("(1234KB)", decoded_response)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_published_document_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_no_size(self, mock_get_document_by_uri, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns an empty string (implying that the file doesn't
        exist in S3), so we should link to our generated PDF instead and not S3."""

        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = ""

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertNotIn("test_2023_123.pdf", decoded_response)
        self.assertIn("/test/2023/123/data.pdf", decoded_response)


@pytest.mark.django_db
class TestDocumentDownloadOptions:
    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    @pytest.mark.parametrize(
        "uri,document_type",
        [("eat/2023/1/press-summary/1", "press summary"), ("eat/2023/1", "judgment")],
    )
    def test_download_options(
        self,
        mock_get_document_by_uri,
        mock_get_pdf_size,
        mock_get_pdf_uri,
        uri,
        document_type,
    ):
        """
        GIVEN a document
        WHEN a request is made with document uri
        THEN html response should contain the download options div
        AND this contains the Download PDF button
        AND this contains the Download XML button
        AND the descriptions refer to the document's type
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri=uri, is_published=True
        )
        mock_get_pdf_size.return_value = "(112KB)"
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"
        client = Client()
        response = client.get(f"/{uri}")
        download_options_html = f"""
        <div id="download-options" class="judgment-download-options">
        <h2 class="judgment-download-options__header">Download options</h2>
        <div class="judgment-download-options__options-list">
            <div class="judgment-download-options__download-option">
            <h3><a href="http://example.com/test.pdf">Download this {document_type} as a PDF (112KB)</a></h3>
            <p>The original format of the {document_type} as handed down by the court, for printing and downloading.</p>
            </div>
            <div class="judgment-download-options__download-option">
            <h3><a href="/{uri}/data.xml">Download this {document_type} as XML</a></h3>
            <p>
            The {document_type} in machine-readable LegalDocML format for developers, data scientists and researchers.
            </p>
            </div>
        </div>
        </div>
        """
        assert_contains_html(response, download_options_html)


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
    @patch("judgments.views.detail.get_document_by_uri")
    def test_non_canonical_uri_redirects(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="test/1234/567", is_published=True
        )
        response = self.client.get("/test/1234/567/")
        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == "/test/1234/567"


class TestPressSummaryLabel(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_label_when_press_summary(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN press summary
        WHEN request is made with press summary uri
        THEN response should contain the press summary label
        """

        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1/press-summary/1", is_published=True
        )
        response = self.client.get("/eat/2023/1/press-summary/1")
        self.assertContains(
            response,
            '<p class="judgment-toolbar__press-summary-title">Press Summary</p>',
        )

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_no_press_summary_label_when_on_judgment(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN judgment
        WHEN request is made with judgment uri
        THEN response should NOT contain the press summary label
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1", is_published=True
        )
        response = self.client.get("/eat/2023/1")
        self.assertNotContains(
            response,
            '<p class="judgment-toolbar__press-summary-title">Press Summary</p>',
        )


@pytest.mark.django_db
class TestViewRelatedDocumentButton:
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    @pytest.mark.parametrize(
        "uri,expected_text,expected_href",
        [
            ("eat/2023/1/press-summary/1", "View Judgment", "eat/2023/1"),
            ("eat/2023/1", "View Press Summary", "eat/2023/1/press-summary/1"),
        ],
    )
    def test_view_related_document_button_when_document_with_related_document(
        self,
        mock_get_document_by_uri,
        mock_get_pdf_size,
        uri,
        expected_text,
        expected_href,
    ):
        """
        GIVEN a document with an associated document
        WHEN a request is made to the document URI
        THEN the response should contain a button linking to the related document
        """

        def get_document_by_uri_side_effect(document_uri):
            if document_uri == uri:
                return JudgmentFactory.build(uri=uri, is_published=True)
            elif document_uri == expected_href:
                return JudgmentFactory.build(uri=expected_href, is_published=True)
            else:
                raise JudgmentNotFoundError()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        expected_html_button = f"""
        <a class="judgment-toolbar-buttons__option--related-document btn-related-document"
            role="button" draggable="false"
            href="/{expected_href}"
        >
            {expected_text}
            <span style="font-weight:normal;font-size:0.9rem"></span>
        </a>
        """
        client = Client()
        response = client.get(f"/{uri}")
        assert_contains_html(response, expected_html_button)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    @pytest.mark.parametrize(
        "uri,unexpected_text,unexpected_href",
        [
            ("eat/2023/1/press-summary/1", "View Judgment", "eat/2023/1"),
            ("eat/2023/1", "View Press Summary", "eat/2023/1/press-summary/1"),
        ],
    )
    def test_no_view_related_document_button_when_document_without_related_document(
        self,
        mock_get_document_by_uri,
        mock_get_pdf_size,
        uri,
        unexpected_text,
        unexpected_href,
    ):
        """
        GIVEN a document without an associated document
        WHEN a request is made to the document URI
        THEN the response should not contain a button linking to the related judgment
        """

        def get_document_by_uri_side_effect(document_uri):
            if document_uri == uri:
                return JudgmentFactory.build(uri=document_uri, is_published=True)
            else:
                raise JudgmentNotFoundError()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        unexpected_html_button = f"""
        <a class="judgment-toolbar-buttons__option--related-document btn-related-document"
            role="button" draggable="false"
            href="/{unexpected_href}"
        >
            {unexpected_text}
            <span style="font-weight:normal;font-size:0.9rem"></span>
        </a>
        """

        client = Client()
        response = client.get(f"/{uri}")
        assert_not_contains_html(response, unexpected_html_button)


@pytest.mark.django_db
class TestBreadcrumbs:
    client = Client(raise_request_exception=False)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_breadcrumb_when_press_summary(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a press summary
        WHEN a request is made with the press summary URI
        THEN the response should contain breadcrumbs including the press summary name
        AND an additional `Press Summary` breadcrumb
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1/press-summary/1",
            is_published=True,
            name="Press Summary of Judgment A",
        )
        response = self.client.get("/eat/2023/1/press-summary/1")
        breadcrumb_html = """
        <div class="page-header__breadcrumb">
            <nav class="page-header__breadcrumb-flex-container" aria-label="Breadcrumb">
                <ol>
                    <li>
                        <span class="page-header__breadcrumb-you-are-in">You are in:</span>
                        <a href="/">Find case law</a>
                    </li>
                    <li><a href="/eat/2023/1">Judgment A</a></li>
                    <li>Press Summary</li>
                </ol>
            </nav>
        </div>
        """
        assert_contains_html(response, breadcrumb_html)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_breadcrumb_when_judgment(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a judgment
        WHEN a request is made with the judgment URI
        THEN the response should contain breadcrumbs including the judgment name
        AND NOT contain an additional `Press Summary` breadcrumb
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1",
            is_published=True,
            name="Judgment A",
        )
        response = self.client.get("/eat/2023/1")
        breadcrumb_html = """
        <div class="page-header__breadcrumb">
            <nav class="page-header__breadcrumb-flex-container" aria-label="Breadcrumb">
            <ol>
                <li>
                    <span class="page-header__breadcrumb-you-are-in">You are in:</span>
                    <a href="/">Find case law</a>
                </li>
                <li>Judgment A</li>
            </ol>
            </nav>
        </div>"""
        assert_contains_html(response, breadcrumb_html)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    @pytest.mark.parametrize(
        "http_error,expected_breadcrumb",
        [
            (JudgmentNotFoundError, "Page not found"),
            (Exception, "Server Error"),
        ],
    )
    def test_breadcrumb_when_errors(
        self,
        mock_get_document_by_uri,
        mock_get_pdf_size,
        http_error,
        expected_breadcrumb,
    ):
        """
        GIVEN an URI matching the detail URI structure but does not match a valid document
        WHEN a request is made with the URI
        THEN the response should contain breadcrumbs including the appropriate error reference
        """

        def get_document_by_uri_side_effect(document_uri):
            raise http_error()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        response = self.client.get("/eat/2023/1")
        breadcrumb_html = f"""
        <div class="page-header__breadcrumb">
            <nav class="page-header__breadcrumb-flex-container" aria-label="Breadcrumb">
            <ol>
                <li>
                    <span class="page-header__breadcrumb-you-are-in">You are in:</span>
                    <a href="/">Find case law</a>
                </li>
                <li>{expected_breadcrumb}</li>
            </ol>
            </nav>
        </div>"""
        assert_contains_html(response, breadcrumb_html)


class TestDocumentHeadings(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_document_headings_when_press_summary(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a press summary and related judgment
        WHEN a request is made with the press summary URI
        THEN the response should contain the heading HTML with the press summary
            name without the "Press Summary of " prefix"
        AND a p tag subheading with the related judgment's NCN
        """

        def get_document_by_uri_side_effect(document_uri):
            if document_uri == "eat/2023/1/press-summary/1":
                return JudgmentFactory.build(
                    uri="eat/2023/1/press-summary/1",
                    is_published=True,
                    name="Press Summary of Judgment A (with some slightly different wording)",
                    neutral_citation="",
                )
            elif document_uri == "eat/2023/1":
                return JudgmentFactory.build(
                    uri="eat/2023/1",
                    is_published=True,
                    name="Judgment A",
                    neutral_citation="Judgment_A_NCN",
                )
            else:
                raise JudgmentNotFoundError()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect
        response = self.client.get("/eat/2023/1/press-summary/1")
        headings_html = """
        <h1 class="judgment-toolbar__title">Judgment A (with some slightly different wording)</h1>
        <p class="judgment-toolbar__reference">Judgment_A_NCN</p>
        """
        assert_contains_html(response, headings_html)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_document_headings_when_judgment(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a judgment exists with URI "eat/2023/1"
        WHEN a request is made with the judgment URI "/eat/2023/1"
        THEN the response should contain the heading HTML with the judgment name
        AND a p tag subheading with the judgment's NCN
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1",
            is_published=True,
            name="Judgment A",
            neutral_citation="Judgment_A_NCN",
        )
        response = self.client.get("/eat/2023/1")
        headings_html = """
        <h1 class="judgment-toolbar__title">Judgment A</h1>
        <p class="judgment-toolbar__reference">Judgment_A_NCN</p>
        """
        assert_contains_html(response, headings_html)


class TestHTMLTitle(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_html_title_when_press_summary(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a press summary
        WHEN a request is made with the press summary URI
        THEN the response should have an HTML title containing the press summary name and "- Find case law"
        """

        def get_document_by_uri_side_effect(document_uri):
            if document_uri == "eat/2023/1/press-summary/1":
                return JudgmentFactory.build(
                    uri="eat/2023/1/press-summary/1",
                    is_published=True,
                    name="Press Summary of Judgment A (with some slightly different wording)",
                )
            elif document_uri == "eat/2023/1":
                return JudgmentFactory.build(
                    uri="eat/2023/1",
                    is_published=True,
                    name="Judgment A",
                )
            else:
                raise JudgmentNotFoundError()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect
        response = self.client.get("/eat/2023/1/press-summary/1")
        html_title = "<title>Press Summary of Judgment A (with some slightly different wording) - Find case law</title>"
        assert_contains_html(response, html_title)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_document_by_uri")
    def test_html_title_when_judgment(
        self, mock_get_document_by_uri, mock_get_pdf_size
    ):
        """
        GIVEN a judgment
        WHEN a request is made with the judgment URI
        THEN the response should have an HTML title containing the judgment name and  "- Find case law"
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri="eat/2023/1",
            is_published=True,
            name="Judgment A",
        )
        response = self.client.get("/eat/2023/1")
        html_title = "<title>Judgment A - Find case law</title>"
        assert_contains_html(response, html_title)
