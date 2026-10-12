from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from lxml import html

from judgments.tests.fixture_data import FakeSearchResponse
from judgments.views.search.scope_preference import SEARCH_SCOPE_PREFERENCE_COOKIE


class TestSearchScopePreference(TestCase):
    @patch("judgments.views.index.cached_recent_judgments")
    def test_homepage_preselects_saved_scope(self, mock_recent):
        mock_recent.return_value = FakeSearchResponse()
        for saved, expected in [
            (None, "all_courts"),
            ("all_courts", "all_courts"),
            ("higher_courts", "higher_courts"),
            ("other_courts", "all_courts"),
            ("invalid", "all_courts"),
        ]:
            with self.subTest(saved=saved):
                self.client.cookies.clear()
                if saved is not None:
                    self.client.cookies[SEARCH_SCOPE_PREFERENCE_COOKIE] = saved
                response = self.client.get(reverse("home"))
                document = html.fromstring(response.content)
                self.assertEqual(document.xpath('//input[@name="scope"][@checked]/@value'), [expected])
                self.assertNotIn(SEARCH_SCOPE_PREFERENCE_COOKIE, response.cookies)
                self.assertIn("Cookie", response.headers["Vary"])
                self.assertEqual(
                    set(response.headers["Cache-Control"].split(", ")), {"private", "no-cache", "max-age=0"}
                )

    @patch("judgments.views.search.results.search_judgments_and_parse_response")
    def test_valid_submission_saves_scope(self, mock_search):
        mock_search.return_value = FakeSearchResponse()
        for scope in ["higher_courts", "all_courts"]:
            with self.subTest(scope=scope):
                response = self.client.get(
                    reverse("search"), {"scope": scope, "save_search_scope_preference": "1"}, secure=True
                )
                self.assertEqual(response.status_code, 200)
                cookie = response.cookies[SEARCH_SCOPE_PREFERENCE_COOKIE]
                self.assertEqual(cookie.value, scope)

    @patch("judgments.views.search.results.search_judgments_and_parse_response")
    def test_invalid_scope_save_submission_not_saved(self, mock_search):
        mock_search.return_value = FakeSearchResponse()
        for scope in [[], ["invalid"], ["other_courts"], ["all_courts", "higher_courts"]]:
            with self.subTest(scope=scope):
                response = self.client.get(
                    reverse("search"), {"scope": scope, "save_search_scope_preference": "1"}, secure=True
                )
                self.assertNotIn(SEARCH_SCOPE_PREFERENCE_COOKIE, response.cookies)
