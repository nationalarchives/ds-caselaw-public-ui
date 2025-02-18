from unittest.mock import patch

import pytest
from django.http import Http404
from django.test import TestCase

from config.views.schema import schema


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


class TestSchemas(TestCase):
    @patch("config.views.schema.requests.get")
    def test_cached(self, get):
        # Tests caching behaviour; happy path
        "We return a 200 with the content but only call it once"
        get.return_value.status_code = 200
        get.return_value.content = b"content-a"
        response = self.client.get("/schema/akn-modified.xsd")
        assert response.content == b"content-a"
        assert response.status_code == 200
        response = self.client.get("/schema/akn-modified.xsd")
        get.assert_called_once()

    @patch("config.views.schema.requests.get")
    def test_error_gives_404(self, get):
        # Does not test caching behaviour and needs to not use an old filename
        "We handle errors from Github correctly"
        get.return_value.status_code = 419
        get.return_value.content = b"content-b"
        with pytest.raises(Http404):
            schema(None, "caselaw.xsd")

    @patch("config.views.schema.requests.get")
    def test_bad_url(self, get):
        # Doesn't care either way about caching
        "Given a bad URL, we don't request anything"
        response = self.client.get("/schema/bad-url.xsd")
        assert response.status_code == 404
        get.assert_not_called()

    @patch("config.views.schema.requests.get")
    def test_no_cache_errors(self, get):
        # Tests caching behaviour -- uses different URI for that reason
        "Errors downloading the document aren't persistent"
        with patch("config.views.schema.requests.get") as get_bad:
            get_bad.return_value.status_code = 419
            get_bad.return_value.content = b"content-c"
            response = self.client.get("/schema/xml.xsd")
            assert response.status_code == 404
        with patch("config.views.schema.requests.get") as get_good:
            get_good.return_value.status_code = 200
            get_good.return_value.content = b"content-d"
            response = self.client.get("/schema/xml.xsd")
        assert response.status_code == 200
        assert response.content == b"content-d"
        get_bad.assert_called_once()
        get_good.assert_called_once()
