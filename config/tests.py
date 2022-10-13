from django.test import TestCase


class TestRedirect(TestCase):
    def test_slash_redirection_works(self):
        url = "/arbitrary/url/with/slash/at/end/"
        response = self.client.get(url)
        assert response.status_code == 302
        assert response.url == url.rstrip("/")

    def test_no_infinite_loop(self):
        url = "/2022/202"
        response = self.client.get(url)
        assert response.status_code == 404
