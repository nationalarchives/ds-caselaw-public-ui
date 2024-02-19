import unittest
from unittest import mock

from caselawclient.errors import DocumentNotFoundError

from judgments.tests.factories import JudgmentFactory, PressSummaryFactory
from judgments.utils import (
    formatted_document_uri,
    get_document_by_uri,
    get_press_summaries_for_document_uri,
    linked_doc_title,
    linked_doc_url,
    press_summary_list_breadcrumbs,
)


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

    def test_linked_doc_url_returns_press_summary_for_a_judgement(self):
        document = JudgmentFactory.build()

        assert linked_doc_url(document) == document.uri + "/press-summary/1"

    def test_linked_doc_url_returns_judgement_for_a_press_summary(self):
        document = PressSummaryFactory.build(uri="/foo/bar/press-summary/1")

        assert linked_doc_url(document) == "/foo/bar"

    def test_linked_doc_title_removes_prefix_for_press_summary(self):
        document = PressSummaryFactory.build(name="Press Summary of Arkell v Pressdram")
        assert linked_doc_title(document) == "Arkell v Pressdram"

    def test_linked_doc_title_adds_prefix_for_judgment(self):
        document = JudgmentFactory.build(name="Arkell v Pressdram")
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

    @mock.patch("judgments.utils.api_client")
    def test_get_press_summaries_for_document_uri(self, mock_api_client):
        summaries = [mock.Mock(), mock.Mock()]
        mock_api_client.get_press_summaries_for_document_uri.return_value = summaries

        result = get_press_summaries_for_document_uri("sample_uri")
        self.assertEqual(result, summaries)
