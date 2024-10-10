import unittest
from unittest import mock
from unittest.mock import Mock

from caselawclient.errors import DocumentNotFoundError
from caselawclient.factories import DocumentBodyFactory, JudgmentFactory, PressSummaryFactory
from caselawclient.models.documents import DocumentURIString
from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import CourtCode

from judgments.utils import (
    formatted_document_uri,
    get_document_by_uri,
    get_press_summaries_for_document_uri,
    linked_doc_title,
    linked_doc_url,
    press_summary_list_breadcrumbs,
    process_court_facets,
    process_year_facets,
    show_no_exact_ncn_warning,
)
from judgments.utils.utils import get_document_by_uri_from_cache


class TestUtils(unittest.TestCase):
    @mock.patch("judgments.utils.utils.api_client")
    def test_get_existing_document(self, mock_api_client):
        document = mock.Mock()
        mock_api_client.get_document_by_uri.return_value = document
        result = get_document_by_uri("sample_uri")
        self.assertEqual(result, document)

    @mock.patch("judgments.utils.utils.api_client")
    def test_get_nonexistent_document(self, mock_api_client):
        mock_api_client.get_document_by_uri.side_effect = DocumentNotFoundError
        with self.assertRaises(DocumentNotFoundError):
            get_document_by_uri("nonexistent_uri")

    @mock.patch("judgments.utils.utils.api_client")
    def test_get_document_by_uri_from_cache_where_document_not_found_and_response_is_not_cachable(
        self, mock_api_client
    ):
        mock_api_client.get_document_by_uri.side_effect = DocumentNotFoundError
        with self.assertRaises(DocumentNotFoundError):
            get_document_by_uri_from_cache("nonexistent_uri", cache_if_not_found=False)

    @mock.patch("judgments.utils.utils.api_client")
    def test_get_document_by_uri_from_cache_where_document_not_found_and_response_is_cachable(self, mock_api_client):
        mock_api_client.get_document_by_uri.side_effect = DocumentNotFoundError
        assert get_document_by_uri_from_cache("nonexistent_uri", cache_if_not_found=True) is None

    def test_formatted_document_uri(self):
        test_params = [
            ("pdf", "/data.pdf"),
            ("generated_pdf", "/generated.pdf"),
            ("xml", "/data.xml"),
            ("html", "/data.html"),
        ]
        document_uri = DocumentURIString("ewhc/comm/2024/253")
        for format, suffix in test_params:
            with self.subTest(format=format, suffix=suffix):
                self.assertEqual(
                    formatted_document_uri(document_uri, format),
                    "/" + document_uri + suffix,
                )

    def test_linked_doc_url_returns_press_summary_for_a_judgement(self):
        document = JudgmentFactory.build()

        assert linked_doc_url(document) == document.uri + "/press-summary/1"

    def test_linked_doc_url_returns_judgement_for_a_press_summary(self):
        document = PressSummaryFactory.build(uri="/foo/bar/press-summary/1")

        assert linked_doc_url(document) == "foo/bar"

    def test_linked_doc_title_removes_prefix_for_press_summary(self):
        document = PressSummaryFactory.build(body=DocumentBodyFactory.build(name="Press Summary of Arkell v Pressdram"))
        assert linked_doc_title(document) == "Arkell v Pressdram"

    def test_linked_doc_title_adds_prefix_for_judgment(self):
        document = JudgmentFactory.build(body=DocumentBodyFactory.build(name="Arkell v Pressdram"))
        assert linked_doc_title(document) == "Press Summary of Arkell v Pressdram"

    def test_press_summary_list_breadcrumbs(self):
        document = PressSummaryFactory.build()

        assert press_summary_list_breadcrumbs(document) == [
            {
                "url": "/" + linked_doc_url(document),
                "text": linked_doc_title(document),
            },
            {
                "text": "Press Summaries",
            },
        ]

    @mock.patch("judgments.utils.utils.api_client")
    def test_get_press_summaries_for_document_uri(self, mock_api_client):
        summaries = [mock.Mock(), mock.Mock()]
        mock_api_client.get_press_summaries_for_document_uri.return_value = summaries

        result = get_press_summaries_for_document_uri("sample_uri")
        self.assertEqual(result, summaries)

    def test_show_warning_when_ncn_query_has_no_exact_matches(
        self,
    ):
        def mock_judgment(ncn):
            mock = Mock()
            mock.configure_mock(neutral_citation=ncn)
            return mock

        query_text = "[2014] EWHC 4122 (Fam)"
        page = 1
        search_results = [mock_judgment(ncn) for ncn in ["[2013] EWSC 123", "[2022] EWHC 54321 (Fam)"]]
        result = show_no_exact_ncn_warning(search_results, query_text, page)
        self.assertTrue(result)

    def test_do_not_show_warning_beyond_first_page(
        self,
    ):
        def mock_judgment(ncn):
            mock = Mock()
            mock.configure_mock(neutral_citation=ncn)
            return mock

        query_text = "[2014] EWHC 4122 (Fam)"
        page = 2
        search_results = [mock_judgment(ncn) for ncn in ["[2013] EWSC 123", "[2022] EWHC 54321 (Fam)"]]
        result = show_no_exact_ncn_warning(search_results, query_text, page)
        self.assertFalse(result)

    def test_do_not_show_warning_when_ncn_query_has_exact_matches(
        self,
    ):
        def mock_judgment(ncn):
            mock = Mock()
            mock.configure_mock(neutral_citation=ncn)
            return mock

        query_text = "[2014] EWHC 4122 (Fam)"
        page = 1
        search_results = [mock_judgment(ncn) for ncn in ["[2013] EWSC 123", "[2014] EWHC 4122 (Fam)"]]
        result = show_no_exact_ncn_warning(search_results, query_text, page)
        self.assertFalse(result)

    def test_do_not_show_warning_when_query_is_not_ncn(self):
        def mock_judgment(ncn):
            mock = Mock()
            mock.configure_mock(neutral_citation=ncn)
            return mock

        query_text = "walrus"
        page = 1
        search_results = [mock_judgment(ncn) for ncn in ["[2013] EWSC 123", "[2014] EWHC 4122 (Fam)"]]
        result = show_no_exact_ncn_warning(search_results, query_text, page)
        self.assertFalse(result)


class TestSearchUtils(unittest.TestCase):
    def test_process_court_facets(self):
        """
        process_court_facets returns court facets, and invalid facets.
        """
        raw_facets = {"EAT": "3", "EWHC-KBD-TCC": "20", "INVALID": "5", "": "1"}
        court_code = all_courts.get_by_code(CourtCode("EWHC-KBD-TCC"))
        tribunal_code = all_courts.get_by_code(CourtCode("EAT"))

        remaining_facets, court_facets, tribunal_facets = process_court_facets(raw_facets)

        self.assertEqual(remaining_facets, {"INVALID": "5", "": "1"})
        self.assertEqual(court_facets, {court_code: "20"})
        self.assertEqual(tribunal_facets, {tribunal_code: "3"})

    def test_process_year_facets(self):
        """
        process_year_facets returns year facets, and invalid facets.
        """
        raw_facets = {"EAT": "3", "2010": "103", "1900": "4"}

        remaining_facets, year_facets = process_year_facets(raw_facets)

        self.assertEqual(remaining_facets, {"EAT": "3", "1900": "4"})
        self.assertEqual(year_facets, {"2010": "103"})
