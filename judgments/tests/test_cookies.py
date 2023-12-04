from http.cookies import SimpleCookie
from unittest.mock import patch

from django.test import TestCase

from judgments.tests.fixtures import FakeSearchResponse


class TestBadCookie(TestCase):
    @patch("judgments.views.index.api_client")
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_bad_cookie(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        self.client.cookies = SimpleCookie({"cookies_policy": "evil"})
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/")
        assert response.status_code == 400
        assert b"Bad Request (400)" in response.content
