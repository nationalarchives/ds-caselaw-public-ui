from unittest.mock import patch

from django.template import engines
from django.test import TestCase, override_settings
from jinja2 import ChoiceLoader, DictLoader


class TestStorybookRenderView(TestCase):
    def test_renders_button_with_application_helpers(self):
        response = self.client.post(
            "/storybook-render",
            {"template": "components/button.jinja", "macro": "button_variant_examples"},
            content_type="application/json",
        )

        self.assertContains(response, 'class="button button--secondary"')
        self.assertContains(response, "Secondary button")
        self.assertNotContains(response, "href=")

    def test_uses_configured_environment_and_request_context(self):
        env = engines["jinja"].env
        loader = DictLoader(
            {
                "storybook_test.jinja": (
                    "{% macro example() %}"
                    '{{ component_class_names("one", "two") }}|{{ "hello world"|hyphenate }}|'
                    "{{ request.path }}|{{ cookie_domain }}"
                    "{% endmacro %}"
                ),
            }
        )
        with patch.object(env, "loader", ChoiceLoader([loader, env.loader])):
            response = self.client.post(
                "/storybook-render",
                {"template": "storybook_test.jinja", "macro": "example"},
                content_type="application/json",
            )

        self.assertContains(response, "one two|hello-world|/storybook-render|testserver")

    def test_ignores_unused_macro_arguments(self):
        expected = self.client.post(
            "/storybook-render",
            {"template": "components/button.jinja", "macro": "button_variant_examples"},
            content_type="application/json",
        )
        response = self.client.post(
            "/storybook-render",
            {
                "template": "components/button.jinja",
                "macro": "button_variant_examples",
                "label": "<script>alert(1)</script>",
                "variant": "unused-variant",
                "size": "unused-size",
            },
            content_type="application/json",
        )

        self.assertContains(response, "Secondary button")
        self.assertEqual(response.content, expected.content)

    def test_render_failure_returns_error_status(self):
        with self.assertLogs("config.views.storybook", level="ERROR"):
            response = self.client.post(
                "/storybook-render",
                {"template": "components/missing.jinja", "macro": "example"},
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Internal server error"})

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
