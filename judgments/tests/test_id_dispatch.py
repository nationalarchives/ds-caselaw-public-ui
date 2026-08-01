from unittest.mock import patch

from caselawclient.factories import JudgmentFactory
from caselawclient.models.identifiers.neutral_citation import NeutralCitationNumber
from django.test import RequestFactory
from fixtures import TestCaseWithMockAPI

from judgments.resolvers.id_dispatch import representation_kind_from_accept


class TestRepresentationKindFromAccept(TestCaseWithMockAPI):
    def test_defaults_to_html_when_accept_missing(self):
        request = RequestFactory().get("/id/d-a1b2c3")
        assert representation_kind_from_accept(request) == "html"

    def test_html_preferred_over_xml_in_browser_style_accept(self):
        request = RequestFactory().get(
            "/id/d-a1b2c3",
            HTTP_ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        )
        assert representation_kind_from_accept(request) == "html"

    def test_akn_xml(self):
        request = RequestFactory().get("/id/d-a1b2c3", HTTP_ACCEPT="application/akn+xml")
        assert representation_kind_from_accept(request) == "xml"

    def test_application_xml(self):
        request = RequestFactory().get("/id/d-a1b2c3", HTTP_ACCEPT="application/xml")
        assert representation_kind_from_accept(request) == "xml"

    def test_pdf(self):
        request = RequestFactory().get("/id/d-a1b2c3", HTTP_ACCEPT="application/pdf")
        assert representation_kind_from_accept(request) == "pdf"

    def test_star_star_defaults_to_html(self):
        request = RequestFactory().get("/id/d-a1b2c3", HTTP_ACCEPT="*/*")
        assert representation_kind_from_accept(request) == "html"

    def test_unsupported_type_returns_none(self):
        request = RequestFactory().get("/id/d-a1b2c3", HTTP_ACCEPT="application/json")
        assert representation_kind_from_accept(request) is None

    def test_unsupported_then_html_still_html(self):
        request = RequestFactory().get(
            "/id/d-a1b2c3",
            HTTP_ACCEPT="application/json,text/html;q=0.5",
        )
        assert representation_kind_from_accept(request) == "html"


class TestIdDispatchEngine(TestCaseWithMockAPI):
    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_redirects_to_preferred_html_by_default(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2025] UKSC 123")]
        )

        response = self.client.get("/id/d-a1b2c3")

        mock_get_document_by_uri.assert_called_once_with("d-a1b2c3")
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers.get("Location"), "/uksc/2025/123")
        self.assertEqual(response.headers.get("Vary"), "Accept")

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_redirects_to_xml_when_accept_akn(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2025] UKSC 123")]
        )

        response = self.client.get("/id/d-a1b2c3", HTTP_ACCEPT="application/akn+xml")

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers.get("Location"), "/uksc/2025/123/data.xml")

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_redirects_to_pdf_when_accept_pdf(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2025] UKSC 123")]
        )

        response = self.client.get("/id/d-a1b2c3", HTTP_ACCEPT="application/pdf")

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers.get("Location"), "/uksc/2025/123/data.pdf")

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_legacy_document_uri_path(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2024] EWHC 253 (Comm)")]
        )

        response = self.client.get("/id/ewhc/comm/2024/253")

        mock_get_document_by_uri.assert_called_once_with("ewhc/comm/2024/253")
        self.assertEqual(response.status_code, 303)

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_500_without_preferred_identifier(self, mock_get_document_by_uri):
        """Published documents without a preferred identifier are broken data → 500."""
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True, identifiers=[])

        with self.assertRaises(RuntimeError):
            # Django's test client converts uncaught exceptions to 500 responses
            # only when DEBUG is False; assert the underlying failure directly.
            self.client.get("/id/d-a1b2c3")

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_406_when_accept_is_unsupported(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2025] UKSC 123")]
        )

        response = self.client.get("/id/d-a1b2c3", HTTP_ACCEPT="application/json")

        self.assertEqual(response.status_code, 406)
        self.assertIsNone(response.headers.get("Location"))
        self.assertEqual(response.headers.get("Vary"), "Accept")
