from os import environ
from typing import Optional
from unittest.mock import call, patch

import pytest
from caselawclient.errors import DocumentNotFoundError
from caselawclient.factories import DocumentBodyFactory, JudgmentFactory, PressSummaryFactory
from caselawclient.models.documents import DocumentURIString
from caselawclient.models.identifiers.neutral_citation import NeutralCitationNumber
from caselawclient.models.identifiers.press_summary_ncn import PressSummaryRelatedNCNIdentifier
from django.http import Http404
from django.template.defaultfilters import filesizeformat
from django.test import Client
from fixtures import MockAPI, TestCaseWithMockAPI

from judgments.tests.utils.assertions import (
    assert_contains_html,
    assert_response_contains_text,
    assert_response_not_contains_text,
)
from judgments.views.detail import (
    PdfDetailView,
)


class TestWeasyWithoutCSS(TestCaseWithMockAPI):
    @patch("judgments.views.detail.generated_pdf.get_document_download_filename")
    @patch.object(PdfDetailView, "pdf_stylesheets", [])
    @patch("judgments.views.detail.generated_pdf.get_published_document_by_uri")
    def test_weasy_without_css_runs_in_ci(self, mock_get_document_by_uri, mock_get_filename):
        mock_get_filename.return_value = "some_download_filename"
        judgment = JudgmentFactory.build(is_published=True)
        mock_get_document_by_uri.return_value = judgment
        response = self.client.get("/eat/2023/1/generated.pdf")
        assert response.status_code == 200
        assert b"%PDF-1.7" in response.content


class TestJudgment(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_published_judgment_response(self, mock_get_document_by_uri, mock_pdf):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True,
            body=DocumentBodyFactory.build(),
        )
        mock_pdf.return_value.size = 1234

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow,noai")

        self.assertIn("This is a document.", decoded_response)
        self.assertIn('<meta name="robots" content="noindex,nofollow,noai" />', decoded_response)

        self.assertEqual(response.status_code, 200)

    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_query_passed_to_api_client(self, mock_get_document_by_uri, mock_pdf):
        judgment = JudgmentFactory.build()

        mock_get_document_by_uri.return_value = judgment

        response = self.client.get("/test/2023/123?query=Query")

        assert mock_get_document_by_uri.mock_calls[0] == call(
            "ml-test/2023/123", search_query="Query"
        )  # We do make subsequent calls as part of getting related documents, but they're not relevant here

        self.assertEqual(response.status_code, 200)


class TestJudgmentBackToSearchLink(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_no_link_if_no_context(self, mock_get_document_by_uri, mock_pdf):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf.return_value.size = 1234

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        assert "Back to search results" not in decoded_response


class TestJudgmentPdfLinkText(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_size(self, mock_get_document_by_uri, mock_pdf):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf.return_value.uri = "https://example.com/test/2023/123/test_2023_123.pdf"
        mock_pdf.return_value.size = 1234

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertIn("/tna.tn4t35ts/data.pdf", decoded_response)
        self.assertIn(f"({filesizeformat(1234)})", decoded_response)

    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_no_size(self, mock_get_document_by_uri, mock_pdf):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf.return_value.uri = "/test/2023/123/data.pdf"
        mock_pdf.return_value.size = None

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertNotIn("test_2023_123.pdf", decoded_response)
        self.assertIn("/tna.tn4t35ts/data.pdf", decoded_response)


class TestDocumentDownloadOptions(MockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf")
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @pytest.mark.parametrize(
        "uri,document_factory_class",
        [("eat/2023/1/press-summary", PressSummaryFactory), ("eat/2023/1", JudgmentFactory)],
    )
    def test_download_options(
        self,
        mock_get_document_by_uri,
        mock_pdf,
        uri,
        document_factory_class,
    ):
        """
        GIVEN a document
        WHEN a request is made with document uri
        THEN html response should contain the download options div
        AND this contains the Download PDF button
        AND this contains the Download XML button
        AND the descriptions refer to the document's type
        """
        mock_get_document_by_uri.return_value = document_factory_class.build(
            uri=uri, is_published=True, body=DocumentBodyFactory.build()
        )
        mock_pdf.return_value.size = 112
        mock_pdf.return_value.uri = "http://example.com/test.pdf"
        document = mock_get_document_by_uri()
        document_title = document.body.name
        document_noun = document.document_noun
        assert document_noun in ["press summary", "judgment"]
        client = Client()
        response = client.get(f"/{uri}")

        download_options_html = f"""
        <section id="download-options" class="judgment-download-options" aria-labelledby="judgment-download-options-header">
            <h2 id="judgment-download-options-header" class="judgment-download-options__header">Document download options</h2>
            <div class="judgment-download-options__options-list">
                <div class="judgment-download-options__download-option">
                    <a href="/tna.tn4t35ts/data.pdf" class="btn" aria-label="Download {document_title} as a PDF ({filesizeformat(112)})" download="">
                        Download PDF <span class="btn__label">({filesizeformat(112)})</span>
                    </a>
                    <p>The original format of the {document_noun} as handed down by the court, for printing and downloading.</p>
                </div>
                <div class="judgment-download-options__download-option">
                    <a href="/{document.identifiers.preferred().url_slug}/data.xml" class="btn" aria-label="Download {document_title} as XML">
                        Download XML
                    </a>
                    <p>
                        The {document_noun} in machine-readable LegalDocML format for developers, data scientists and researchers.
                    </p>
                </div>
            </div>
        </section>
        """
        assert_contains_html(response, download_options_html)


class TestPressSummaryLabel(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_label_when_press_summary(self, mock_get_document_by_uri, mock_pdf):
        """
        WHEN a request is made for a document's detail page
        GIVEN the document is a  press summary
        THEN response should contain the press summary label
        """

        mock_get_document_by_uri.return_value = PressSummaryFactory.build(is_published=True)
        response = self.client.get("/test/2023/123")  # has to match factory to avoid redirect.

        xpath_query = "//p[@class='judgment-toolbar__press-summary-title']"
        assert_response_contains_text(response, "Press Summary", xpath_query)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_no_press_summary_label_when_on_judgment(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN judgment
        WHEN request is made with judgment uri
        THEN response should NOT contain the press summary label
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri=DocumentURIString("eat/2023/1"), is_published=True
        )
        response = self.client.get("/eat/2023/1")

        xpath_query = "//p[@class='judgment-toolbar__press-summary-title']"
        assert_response_not_contains_text(response, "Press Summary", xpath_query)


class TestViewRelatedDocumentButton(MockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @pytest.mark.parametrize(
        "uri,expected_text,expected_href,document_class_factory",
        [
            (
                "eat/2023/1/press-summary",
                "View Judgment",
                "/tna.tn4t35ts",
                PressSummaryFactory,
            ),
            (
                "eat/2023/1",
                "View Press Summary",
                "/tna.tn4t35ts",
                JudgmentFactory,
            ),
        ],
    )
    def test_view_related_document_button_when_document_with_related_document(
        self,
        mock_get_document_by_uri,
        mock_pdf,
        uri,
        expected_text,
        expected_href,
        document_class_factory,
    ):
        """
        GIVEN a document with an associated document
        WHEN a request is made to the document URI
        THEN the response should contain a button linking to the related document
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            return document_class_factory.build(uri=document_uri, is_published=True)

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        client = Client()
        response = client.get(f"/{uri}")
        xpath_query = f"//a[@href='{expected_href}']"
        assert_response_contains_text(response, expected_text, xpath_query)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @pytest.mark.parametrize(
        "uri,expected_text,expected_href,document_class_factory",
        [
            (
                "eat/2023/1/press-summary",
                "View Judgment",
                "/tna.tn4t35ts",
                PressSummaryFactory,
            ),
            (
                "eat/2023/1",
                "View Press Summary",
                "/tna.tn4t35ts",
                JudgmentFactory,
            ),
        ],
    )
    def test_view_related_document_button_when_document_with_related_document_and_query_string(
        self,
        mock_get_document_by_uri,
        mock_pdf,
        uri,
        expected_text,
        expected_href,
        document_class_factory,
    ):
        """
        GIVEN a document with an associated document
        WHEN a request is made to the document URI
        THEN the response should contain a button linking to the related document
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            return document_class_factory.build(uri=document_uri, is_published=True)

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        client = Client()
        response = client.get(f"/{uri}?query=Query")
        xpath_query = f"//a[@href='{expected_href}?query=Query']"
        assert_response_contains_text(response, expected_text, xpath_query)
        assert "ml-" not in response.content.decode("utf-8")

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @pytest.mark.parametrize(
        "uri,unexpected_text,unexpected_href",
        [
            ("eat/2023/1/press-summary", "View Judgment", "eat/2023/1"),
            ("eat/2023/1", "View Press Summary", "eat/2023/1/press-summary"),
        ],
    )
    def test_no_view_related_document_button_when_document_without_related_document(
        self,
        mock_get_document_by_uri,
        mock_pdf,
        uri,
        unexpected_text,
        unexpected_href,
    ):
        """
        GIVEN a document without an associated document
        WHEN a request is made to the document URI
        THEN the response should not contain a button linking to the related judgment
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            return JudgmentFactory.build(uri=document_uri, is_published=True, document_noun="press summary")

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        client = Client()
        response = client.get(f"/{uri}")
        xpath_query = f"//a[@href='{unexpected_href}']"
        assert_response_not_contains_text(response, unexpected_text, xpath_query)


@pytest.mark.django_db
class TestBreadcrumbs(MockAPI):
    client = Client(raise_request_exception=False)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_breadcrumb_when_press_summary(self, mock_get_document_by_uri, mock_pdf):
        """
        WHEN a request is made to a document detail page
        GIVEN the document returned is a press summary
        THEN the response should contain breadcrumbs including the press summary name
        AND an additional `Press Summary` breadcrumb
        """

        def get_document_by_uri_side_effect(uri, cache_if_not_found=False, search_query: Optional[str] = None):
            if "press" in uri:
                return PressSummaryFactory.build(
                    uri=DocumentURIString("eat/2023/1/press-summary"),
                    is_published=True,
                    body=DocumentBodyFactory.build(
                        name="Press Summary of Judgment A",
                    ),
                )
            else:
                return JudgmentFactory.build(
                    uri=DocumentURIString("eat/2023/1"),
                    is_published=True,
                    body=DocumentBodyFactory.build(
                        name="The Title of Judgment A",
                    ),
                )

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        response = self.client.get("/eat/2023/1/press-summary")
        judgment_breadcrumb_html = """
                    <li><a href="/tna.tn4t35ts">Judgment A</a></li>
        """

        summary_breadcrumb_html = """
                    <li>Press Summary</li>
        """
        assert_contains_html(response, judgment_breadcrumb_html)
        assert_contains_html(response, summary_breadcrumb_html)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_breadcrumb_when_judgment(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN a judgment
        WHEN a request is made with the judgment URI
        THEN the response should contain breadcrumbs including the judgment name
        AND NOT contain an additional `Press Summary` breadcrumb
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri=DocumentURIString("eat/2023/1"),
            is_published=True,
            body=DocumentBodyFactory.build(
                name="Judgment A",
            ),
        )
        response = self.client.get("/eat/2023/1")
        assert_response_contains_text(response, "Judgment A", "//div[@class='breadcrumbs']")

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    @pytest.mark.parametrize(
        "http_error,expected_breadcrumb",
        [
            (Http404, "Page not found"),
            (Exception, "Server Error"),
        ],
    )
    def test_breadcrumb_when_errors(
        self,
        mock_get_document_by_uri,
        mock_pdf,
        http_error,
        expected_breadcrumb,
    ):
        """
        GIVEN an URI matching the detail URI structure but does not match a valid document
        WHEN a request is made with the URI
        THEN the response should contain breadcrumbs including the appropriate error reference
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            raise http_error()

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect

        response = self.client.get("/eat/2023/1")

        assert_response_contains_text(response, expected_breadcrumb, "//div[@class='breadcrumbs']")


class TestDocumentHeadings(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_document_headings_when_press_summary(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN that the document returned will be a press summary
        WHEN a request is made with to a document detail page
        THEN the response should contain the heading HTML with the press summary
            name without the "Press Summary of " prefix"
        AND a p tag subheading with the related judgment's NCN
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            if document_uri == "ml-eat/2023/1/press-summary":
                press_summary = PressSummaryFactory.build(
                    uri=DocumentURIString("ml-eat/2023/1/press-summary"),
                    is_published=True,
                    body=DocumentBodyFactory.build(
                        name="Press Summary of Judgment A (with some slightly different wording)",
                    ),
                )
                press_summary_ncn = PressSummaryRelatedNCNIdentifier(value="[2023] EAT 1")
                press_summary.identifiers.add(press_summary_ncn)
                return press_summary
            elif document_uri == "ml-eat/2023/1":
                judgment = JudgmentFactory.build(
                    uri=DocumentURIString("ml-eat/2023/1"),
                    is_published=True,
                    body=DocumentBodyFactory.build(
                        name="Judgment A",
                    ),
                )
                judgment_ncn = NeutralCitationNumber(value="[2023] EAT 1")
                judgment.identifiers.add(judgment_ncn)
                return judgment
            else:
                raise DocumentNotFoundError(f"didn't recognise {document_uri}")

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect
        response = self.client.get("/eat/2023/1/press-summary")
        h1_xpath_query = "//h1"
        reference_xpath_query = "//p[@class='judgment-toolbar__reference']"

        assert_response_contains_text(response, "Judgment A (with some slightly different wording)", h1_xpath_query)
        assert_response_contains_text(response, "[2023] EAT 1", reference_xpath_query)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_document_heading_contains_document_title(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN a judgment exists with URI "eat/2023/1"
        WHEN a request is made with the judgment URI "/eat/2023/1"
        THEN the response should contain the heading HTML with the judgment name
        """

        document = JudgmentFactory.build(
            uri=DocumentURIString("eat/2023/1"),
            is_published=True,
            body=DocumentBodyFactory.build(name="Judgment A"),
        )
        mock_get_document_by_uri.return_value = document

        response = self.client.get("/eat/2023/1")
        h1_xpath_query = "//h1"

        assert_response_contains_text(response, "Judgment A", h1_xpath_query)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_document_heading_contains_preferred_human_identifier(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN a judgment exists with URI "eat/2023/1"
        WHEN a request is made with the judgment URI "/eat/2023/1"
        THEN a p tag subheading with the judgment's NCN
        """

        document = JudgmentFactory.build(
            uri=DocumentURIString("eat/2023/1"),
            is_published=True,
            body=DocumentBodyFactory.build(name="Judgment A"),
        )

        document_ncn = NeutralCitationNumber(value="[1234] UKSC 1")
        document.identifiers.add(document_ncn)

        mock_get_document_by_uri.return_value = document

        response = self.client.get("/eat/2023/1")
        reference_xpath_query = "//p[@class='judgment-toolbar__reference']"

        assert_response_contains_text(response, "[1234] UKSC 1", reference_xpath_query)


class TestHTMLTitle(TestCaseWithMockAPI):
    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_html_title_when_press_summary(self, mock_get_document_by_uri, mock_pdf):
        """
        GIVEN a press summary
        WHEN a request is made with the press summary URI
        THEN the response should have an HTML title containing the press
        summary name and "- Find Case Law - The National Archives"
        """

        def get_document_by_uri_side_effect(document_uri, cache_if_not_found=False, search_query: Optional[str] = None):
            if document_uri == "ml-eat/2023/1/press-summary":
                return JudgmentFactory.build(
                    uri=DocumentURIString("ml-eat/2023/1/press-summary"),
                    is_published=True,
                    body=DocumentBodyFactory.build(name="Press Summary of Judgment A"),
                )
            else:
                return JudgmentFactory.build(
                    uri=DocumentURIString("ml-eat/2023/1"),
                    is_published=True,
                    body=DocumentBodyFactory.build(name="Not the press summary"),
                )

        mock_get_document_by_uri.side_effect = get_document_by_uri_side_effect
        response = self.client.get("/eat/2023/1/press-summary")
        title = """
                Press Summary of Judgment A
                - Find Case Law - The National Archives
        """
        xpath_query = "//title"
        assert_response_contains_text(response, title, xpath_query)

    @patch("judgments.views.detail.detail_html.DocumentPdf", autospec=True)
    @patch("judgments.views.detail.detail_html.get_published_document_by_uri")
    def test_html_title_when_judgment(
        self,
        mock_get_document_by_uri,
        mock_pdf,
    ):
        """
        GIVEN a judgment
        WHEN a request is made with the judgment URI
        THEN the response should have an HTML title containing the judgment
        name and  "- Find Case Law - The National Archives"
        """
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            uri=DocumentURIString("eat/2023/1"),
            is_published=True,
            body=DocumentBodyFactory.build(name="Judgment A"),
        )
        response = self.client.get("/eat/2023/1")
        title = "Judgment A - Find Case Law - The National Archives"
        xpath_query = "//title"
        assert_response_contains_text(response, title, xpath_query)
