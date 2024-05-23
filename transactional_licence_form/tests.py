from django.test import TestCase


class TestView(TestCase):
    def test_ok_response(self):
        response = self.client.get("/re-use-find-case-law-records")
        self.assertEqual(response.status_code, 200)
