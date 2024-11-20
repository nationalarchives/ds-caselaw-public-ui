from django.test import TestCase


class TestURLResolution(TestCase):
    def test_trailing_slash(self):
        response = self.client.get("/test/2023/123/")
        assert response.status_code == 404
