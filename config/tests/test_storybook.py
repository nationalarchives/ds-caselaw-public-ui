from django.test import TestCase, override_settings


class TestStorybookRenderView(TestCase):
    @override_settings(STORYBOOK_CORS_ALLOWED_ORIGINS=["https://nationalarchives.github.io"])
    def test_allows_storybook_github_pages_origin(self):
        response = self.client.options(
            "/storybook-render",
            headers={"Origin": "https://nationalarchives.github.io"},
        )

        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Origin"] == "https://nationalarchives.github.io"
        assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
        assert response.headers["Access-Control-Allow-Headers"] == "Content-Type"

    @override_settings(STORYBOOK_CORS_ALLOWED_ORIGINS=["https://nationalarchives.github.io"])
    def test_does_not_allow_unconfigured_origins(self):
        response = self.client.options(
            "/storybook-render",
            headers={"Origin": "https://example.com"},
        )

        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" not in response.headers
