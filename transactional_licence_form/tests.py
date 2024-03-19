from django.test import TestCase


class TestView(TestCase):
    def test_ok_response(self):
        response = self.client.get("/apply-for-a-transactional-licence")
        self.assertEqual(response.status_code, 200)
