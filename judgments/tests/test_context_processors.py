from unittest.mock import patch
from django.test import TestCase
import lxml.html
from waffle.testutils import override_flag


class TestWaffleFlagsProcessor(TestCase):
    def assert_setting(self, option, expected_value):
        assert f"{option}_homepage: {expected_value}" in self.root.xpath(f'//p[@class="test_{option}"]/text()')[0]

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=True)
    @override_flag("v1_homepage", active=True)
    @override_flag("v2_homepage", active=False)
    @override_flag("v3_homepage", active=False)
    def test_variant_v1(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="yes")
        self.assert_setting(option="v1", expected_value="yes")
        self.assert_setting(option="v2", expected_value="no")
        self.assert_setting(option="v3", expected_value="no")

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=True)
    @override_flag("v1_homepage", active=False)
    @override_flag("v2_homepage", active=False)
    @override_flag("v3_homepage", active=False)
    def test_variant_only(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="no")
        self.assert_setting(option="v1", expected_value="no")
        self.assert_setting(option="v2", expected_value="no")
        self.assert_setting(option="v3", expected_value="no")

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=True)
    @override_flag("v1_homepage", active=True)
    @override_flag("v2_homepage", active=True)
    @override_flag("v3_homepage", active=True)
    def test_all_on(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="yes")
        self.assert_setting(option="v1", expected_value="yes")
        self.assert_setting(option="v2", expected_value="no")
        self.assert_setting(option="v3", expected_value="no")

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=False)
    @override_flag("v1_homepage", active=False)
    @override_flag("v2_homepage", active=False)
    @override_flag("v3_homepage", active=False)
    def test_all_off(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="no")
        self.assert_setting(option="v1", expected_value="no")
        self.assert_setting(option="v2", expected_value="no")
        self.assert_setting(option="v3", expected_value="no")

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=True)
    @override_flag("v1_homepage", active=False)
    @override_flag("v2_homepage", active=True)
    @override_flag("v3_homepage", active=True)
    def test_variant_23_on(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="yes")
        self.assert_setting(option="v1", expected_value="no")
        self.assert_setting(option="v2", expected_value="yes")
        self.assert_setting(option="v3", expected_value="no")

    @patch("judgments.views.index.api_client")
    @override_flag("variant_homepage", active=True)
    @override_flag("v1_homepage", active=False)
    @override_flag("v2_homepage", active=False)
    @override_flag("v3_homepage", active=True)
    def test_variant_3_on(self, api_client):
        response = self.client.get("/test-page-please-ignore")
        self.root = lxml.html.fromstring(response.content)
        self.assert_setting(option="variant", expected_value="yes")
        self.assert_setting(option="v1", expected_value="no")
        self.assert_setting(option="v2", expected_value="no")
        self.assert_setting(option="v3", expected_value="yes")
