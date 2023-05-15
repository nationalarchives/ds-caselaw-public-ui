from unittest.mock import patch

from django.test import TestCase

from judgments.tests.test_search import fake_search_result, fake_search_results


class TestHomepage(TestCase):
    @patch("judgments.views.index.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_homepage(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        response = self.client.get("/")
        fake_advanced_search.assert_called_with(order="-date")
        self.assertContains(
            response,
            "A SearchResult name!",
        )
