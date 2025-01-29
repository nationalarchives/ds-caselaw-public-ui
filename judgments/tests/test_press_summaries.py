from unittest.mock import Mock, patch

from caselawclient.factories import PressSummaryFactory
from django.test import TestCase
from django.urls import reverse

from judgments.utils import linked_doc_title, press_summary_list_breadcrumbs
from judgments.views.press_summaries import press_summaries


class TestPressSummaries(TestCase):
    @patch("judgments.views.press_summaries.TemplateResponse", autospec=True)
    @patch("judgments.views.press_summaries.get_press_summaries_for_document_uri")
    def test_view_returns_template_response_for_multiple_press_summaries(
        self, mock_get_press_summaries_for_document_uri, mock_template_response
    ):
        press_summary_1 = PressSummaryFactory.build()
        press_summary_2 = PressSummaryFactory.build()

        expected_press_summaries = [
            press_summary_1,
            press_summary_2,
        ]

        mock_get_press_summaries_for_document_uri.return_value = expected_press_summaries

        request = Mock()
        document_uri = "foo/bar/baz"

        press_summaries(request, document_uri)

        mock_template_response.assert_called_with(
            request,
            "judgment/press_summaries/list.html",
            context={
                "page_title": f"{linked_doc_title(press_summary_1)} - Press Summaries",
                "judgment_name": linked_doc_title(press_summary_1),
                "breadcrumbs": press_summary_list_breadcrumbs(press_summary_1),
                "press_summaries": expected_press_summaries,
            },
        )

    @patch("judgments.views.press_summaries.get_press_summaries_for_document_uri")
    def test_redirects_to_press_summaries_when_one_present(self, mock_get_press_summaries_for_document_uri):
        press_summary = PressSummaryFactory.build()
        mock_get_press_summaries_for_document_uri.return_value = [press_summary]

        response = self.client.get("/uksc/2023/35/press-summary", follow=False)

        self.assertRedirects(
            response,
            reverse(
                "detail",
                kwargs={"document_uri": press_summary.uri},
            ),
            fetch_redirect_response=False,
        )

    @patch("judgments.views.press_summaries.get_press_summaries_for_document_uri")
    def test_shows_multiple_when_multiple_present(self, mock_get_press_summaries_for_document_uri):
        press_summary_1 = PressSummaryFactory.build()
        press_summary_2 = PressSummaryFactory.build()

        mock_get_press_summaries_for_document_uri.return_value = [
            press_summary_1,
            press_summary_2,
        ]

        response = self.client.get("/uksc/2023/35/press-summary")
        decoded_response = response.content.decode("utf-8")

        self.assertIn(
            f"{linked_doc_title(press_summary_1)} - Press Summaries",
            decoded_response,
        )
        self.assertIn(
            press_summary_1.body.name,
            decoded_response,
        )
        self.assertIn(
            press_summary_2.body.name,
            decoded_response,
        )

    @patch("judgments.views.press_summaries.get_press_summaries_for_document_uri")
    def test_throws_404_when_no_summaries_present(self, mock_get_press_summaries_for_document_uri):
        mock_get_press_summaries_for_document_uri.return_value = []

        response = self.client.get("/uksc/2023/35/press-summary")

        assert response.status_code == 404
