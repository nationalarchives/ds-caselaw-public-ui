from unittest import mock

from django.test import TestCase


class MockResponse:
    def __init__(self, xml_data, status_code):
        self.xml_data = xml_data
        self.status_code = status_code

    def text(self):
        return self.xml_data

    def status_code(self):
        return self.status_code


valid_judgment_response = MockResponse(
    (
        '<?xml version="1.0" encoding="UTF-8"?><akomaNtoso>'
        '<judgment name="judgment"><uk:cite>[2004] EWCA Civ 632</uk:cite>'
        "</judgment></akomaNtoso>"
    ),
    200,
)

invalid_judgment_response = MockResponse("anything", 404)


class TestJudgment(TestCase):
    @mock.patch("judgments.views.requests.get", return_value=valid_judgment_response)
    def test_valid_content(self, mock_get):
        response = self.client.get("/judgments/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("[2004] EWCA Civ 632", decoded_response)
        self.assertEqual(response.status_code, 200)

    @mock.patch("judgments.views.requests.get", return_value=invalid_judgment_response)
    def test_404_response(self, mock_get):
        response = self.client.get("/judgments/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("That judgment was not found", decoded_response)
        self.assertEqual(response.status_code, 404)
