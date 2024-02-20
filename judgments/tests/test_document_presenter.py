from unittest.mock import Mock

import pytest
from django.template.defaultfilters import filesizeformat

from judgments.presenters.document_presenter import DocumentPresenter
from judgments.tests.factories import JudgmentFactory, PressSummaryFactory


@pytest.mark.parametrize(
    "document",
    [
        JudgmentFactory.build(),
        PressSummaryFactory.build(),
    ],
)
class TestDocumentPresenter:

    def test_passthrough_properties_get_passed_from_model(self, document):
        document_presenter = DocumentPresenter(document, Mock())

        for key in document_presenter.PASSTHROUGH_PROPERTIES:
            assert getattr(document_presenter, key) == getattr(document, key)

        for key in document_presenter.PASSTHROUGH_ALIASES:
            assert getattr(document_presenter, key) == getattr(
                document, document_presenter.PASSTHROUGH_ALIASES[key]
            )

    def test_number_of_mentions_returns_nothing_without_query(self, document):
        document_presenter = DocumentPresenter(document, Mock())

        assert document_presenter.number_of_mentions is None

    def test_number_of_mentions_calls_number_of_mentions_with_query(self, document):
        query = "query=Query"
        document_presenter = DocumentPresenter(document, Mock(), query)

        assert document_presenter.number_of_mentions == document.number_of_mentions(
            query
        )

    def test_linked_document_uri_returns_linked_uri(self, document):
        document_presenter = DocumentPresenter(document, Mock())
        assert document_presenter.linked_document_uri == document.linked_document.uri

    def test_content_returns_latest_version_as_html(self, document):
        document_presenter = DocumentPresenter(document, Mock())

        assert document_presenter.content == document.content_as_html(
            document_presenter.MOST_RECENT_VERSION, None
        )

    def test_content_returns_latest_version_as_html_when_query_provided(self, document):
        query = "query=query"
        document_presenter = DocumentPresenter(document, Mock(), query)

        assert document_presenter.content == document.content_as_html(
            document_presenter.MOST_RECENT_VERSION, query
        )

    def test_get_pdf_size_returns_formatted_pdf_size(self, document):
        pdf = Mock(size=100)

        document_presenter = DocumentPresenter(document, pdf)

        assert document_presenter.pdf_size == f" ({filesizeformat(pdf.size)})"

    def test_get_pdf_size_returns_blank_string_if_size_null(self, document):
        pdf = Mock(size=None)

        document_presenter = DocumentPresenter(document, pdf)

        assert document_presenter.pdf_size == ""

    def test_returns_pdf_uri_if_exists(self, document):
        pdf = Mock(uri="foo/bar/baz")
        document_presenter = DocumentPresenter(document, pdf)

        assert document_presenter.pdf_uri == "foo/bar/baz"

    def test_breadcrumbs(self, document):
        pdf = Mock()
        document_presenter = DocumentPresenter(document, pdf)

        if document.document_noun == "press summary":
            assert document_presenter.breadcrumbs == [
                {
                    "url": "/" + document.linked_document.uri,
                    "text": document.linked_document.name,
                },
                {
                    "text": "Press Summary",
                },
            ]
        else:
            assert document_presenter.breadcrumbs == [
                {"text": document.name},
            ]
