from django.test import TestCase


class TestJudgment(TestCase):
    def test_valid_content(self):
        response = self.client.get("/judgments/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("[2004] EWCA Civ 632", decoded_response)
        self.assertEqual(response.status_code, 200)

    def test_404_response(self):
        response = self.client.get("/judgments/ewca/civ/2004/63X")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("Judgment was not found", decoded_response)
        self.assertEqual(response.status_code, 404)
