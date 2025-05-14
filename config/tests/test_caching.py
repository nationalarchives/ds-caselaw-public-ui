from django.test import TestCase


class TestCacheHeaders(TestCase):
    def test_static_headers(self):
        url = "/static/images/tna_logo.svg"
        response = self.client.get(url)
        assert response.headers["Cache-Control"] == "max-age=900, public"

    def test_view_headers(self):
        url = "/about-this-service"
        response = self.client.get(url)
        assert response.headers["Cache-Control"] == "max-age=900, public"

    def test_no_cache_transactional_steps(self):
        url = "/re-use-find-case-law-records/steps/organization"
        response = self.client.get(url)
        assert response.headers["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate, public"
