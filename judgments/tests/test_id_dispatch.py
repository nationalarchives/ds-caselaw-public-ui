from unittest.mock import patch

from caselawclient.factories import JudgmentFactory
from caselawclient.models.identifiers.neutral_citation import NeutralCitationNumber
from fixtures import TestCaseWithMockAPI


class TestIdDispatchEngine(TestCaseWithMockAPI):
    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_id_dispatch_for_document(self, mock_get_document_by_uri):
        """Check that IdDispatchEngine tries to retrieve the correct document, and redirects to the right place using the right code."""
        mock_get_document_by_uri.return_value = JudgmentFactory.build(
            is_published=True, identifiers=[NeutralCitationNumber(value="[2025] UKSC 123")]
        )

        response = self.client.get("/id/d-a1b2c3")

        mock_get_document_by_uri.assert_called_once_with("d-a1b2c3")

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers.get("Location"), "/uksc/2025/123")

    @patch("judgments.resolvers.id_dispatch.get_published_document_by_uri")
    def test_id_dispatch_for_document_without_identifiers(self, mock_get_document_by_uri):
        """Check that IdDispatchEngine will return a 404 if a valid document has no identifiers."""
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True, identifiers=[])

        response = self.client.get("/id/d-a1b2c3")

        mock_get_document_by_uri.assert_called_once_with("d-a1b2c3")

        self.assertEqual(response.status_code, 404)
