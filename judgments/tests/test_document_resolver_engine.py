from unittest.mock import patch

from django.test import RequestFactory
from fixtures import TestCaseWithMockAPI

from judgments.resolvers.document_resolver_engine import DocumentResolverEngine


class TestDocumentResolverEngine(TestCaseWithMockAPI):
    @patch("judgments.resolvers.document_resolver_engine.best_pdf")
    @patch("judgments.resolvers.document_resolver_engine.generated_pdf")
    @patch("judgments.resolvers.document_resolver_engine.detail_xml")
    @patch("judgments.resolvers.document_resolver_engine.detail_html")
    def test_resolver_engine_with_fileformats(
        self,
        mock_detail_html,
        mock_detail_xml,
        mock_generated_pdf,
        mock_best_pdf,
    ):
        document_uri = "ewhc/comm/2024/253"
        test_params = [
            ("data.pdf", mock_best_pdf),
            ("generated.pdf", mock_generated_pdf),
            ("data.xml", mock_detail_xml),
            ("data.html", mock_detail_html),
        ]
        for file_format, view in test_params:
            with self.subTest(filename=file_format, view=view):
                path = document_uri + "/" + file_format
                request = RequestFactory().get(path)
                resolver_engine = DocumentResolverEngine()
                resolver_engine.setup(request)
                resolver_engine.dispatch(request, document_uri, file_format=file_format)

                view.assert_called_with(request, document_uri)
