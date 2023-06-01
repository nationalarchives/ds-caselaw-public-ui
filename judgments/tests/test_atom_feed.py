from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixtures import FakeSearchResponse


class TestAtomFeed(TestCase):
    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_feed_exists(
        self, mock_api_client, mock_search_judgments_and_parse_response
    ):
        search_response = FakeSearchResponse()
        mock_search_judgments_and_parse_response.return_value = search_response

        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")

        # that search_judgments_and_parse_response is called with the appropriate parameters
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                court=None,
                date_from=None,
                date_to=None,
                order="-date",
                page=1,
            ),
        )

        # that there is a successful response
        self.assertEqual(response.status_code, 200)
        # that it is an atom feed
        self.assertEqual(
            response["Content-Type"], "application/atom+xml; charset=utf-8"
        )

        # that it has the correct site name
        self.assertIn("<name>The National Archives</name>", decoded_response)
        # that it is like an Atom XML document
        self.assertIn("http://www.w3.org/2005/Atom", decoded_response)
        # that it has an entry
        self.assertIn("<entry>", decoded_response)
        # and it contains actual content - neither neutral citation or court appear in the feed to test.
        self.assertIn("A SearchResult name!", decoded_response)

    @patch("judgments.feeds.search_judgments_and_parse_response")
    def test_bad_page_404(self, mock_search_judgments_and_parse_response):
        # "?page=" 404s, not 500
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/atom.xml?page=")
        self.assertEqual(response.status_code, 404)

    @patch("judgments.feeds.search_judgments_and_parse_response")
    def test_feed_with_empty_date(self, mock_search_judgments_and_parse_response):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("A SearchResult name!", decoded_response)
