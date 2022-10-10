from django.test import TestCase


class TestRedirect(TestCase):
    def test_slash_redirection(self):
        url = "/arbitrary/url/with/slash/at/end/"
        response = self.client.get(url)
        assert response.status_code == 302
        assert response.url == url.rstrip("/")

    def test_lowercase_slash_redirection(self):
        url = "/kitTEN/"
        response = self.client.get(url)
        assert response.status_code == 302
        assert response.url == url.lower().rstrip("/")

    def test_lowercase_redirection(self):
        url = "/kitTEN"
        response = self.client.get(url)
        assert response.status_code == 302
        assert response.url == url.lower()
