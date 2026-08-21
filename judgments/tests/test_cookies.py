from http.cookies import SimpleCookie
from unittest.mock import patch

from django.test import TestCase

from judgments.context_processors import cookie_domain_from_host
from judgments.tests.fixture_data import FakeSearchResponse


class TestBadCookie(TestCase):
    @patch("judgments.views.index.api_client")
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_bad_cookie(self, mock_search_judgments_and_parse_response, mock_api_client):
        self.client.cookies = SimpleCookie({"cookies_policy": "evil"})
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/")
        assert response.status_code == 400
        assert b"Bad Request (400)" in response.content


class TestCookieDomainFromHost(TestCase):
    def test_keeps_localhost_unchanged(self):
        self.assertEqual(cookie_domain_from_host("localhost"), "localhost")
        self.assertEqual(cookie_domain_from_host("localhost:3000"), "localhost")

    def test_keeps_single_label_hosts_unchanged(self):
        self.assertEqual(cookie_domain_from_host("django"), "django")

    def test_keeps_ip_addresses_unchanged(self):
        self.assertEqual(cookie_domain_from_host("127.0.0.1"), "127.0.0.1")
        self.assertEqual(cookie_domain_from_host("[::1]:3000"), "::1")

    def test_returns_root_domain_for_subdomains(self):
        self.assertEqual(cookie_domain_from_host("www.example.com"), ".example.com")
        self.assertEqual(cookie_domain_from_host("service.sub.example.com"), ".example.com")

    def test_returns_root_domain_for_country_code_domains(self):
        self.assertEqual(cookie_domain_from_host("www.nationalarchives.gov.uk"), ".nationalarchives.gov.uk")
        self.assertEqual(cookie_domain_from_host("caselaw.nationalarchives.gov.uk"), ".nationalarchives.gov.uk")
