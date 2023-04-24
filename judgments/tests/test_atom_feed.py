from unittest.mock import patch

from django.test import TestCase
from test_search import fake_search_result, fake_search_results


class TestAtomFeed(TestCase):
    @patch("judgments.feeds.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_feed_exists(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()

        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")
        # that there is a valid page
        self.assertEqual(response.status_code, 200)
        # that it has the correct site name
        self.assertIn("<name>The National Archives</name>", decoded_response)
        # that it is like an Atom XML document
        self.assertIn("http://www.w3.org/2005/Atom", decoded_response)
        # that it has an entry
        self.assertIn("<entry>", decoded_response)
        # and it contains actual content - neither neutral citation or court appear in the feed to test.
        self.assertIn("A SearchResult name!", decoded_response)

    @patch("judgments.utils.perform_advanced_search")
    def test_bad_page_404(self, fake_advanced_search):
        # "?page=" 404s, not 500
        fake_advanced_search.return_value = fake_search_results()
        response = self.client.get("/atom.xml?page=")
        self.assertEqual(response.status_code, 404)
