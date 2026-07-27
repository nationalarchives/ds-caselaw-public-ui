from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase

from config.middleware import LinkHeaderMiddleware


class TestLinkHeaderMiddleware(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_adds_sitewide_and_context_links(self):
        request = self.request_factory.get("/")

        def get_response(_request):
            return TemplateResponse(
                _request,
                template="pages/home.jinja",
                context={
                    "links": [
                        {
                            "href": "/llms.txt",
                            "rel": "describedby",
                            "type": "text/markdown",
                            "title": "Site index for LLMs",
                        }
                    ]
                },
            )

        response = LinkHeaderMiddleware(get_response)(request)

        assert response.headers["Link"] == (
            '</sitemap.xml>; rel="sitemap"; type="application/xml", '
            '</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json", '
            '</llms.txt>; rel="describedby"; type="text/markdown"; title="Site index for LLMs"'
        )

    def test_translates_alternates_to_alternate_link_headers(self):
        request = self.request_factory.get("/")

        def get_response(_request):
            return TemplateResponse(
                _request,
                template="pages/home.jinja",
                context={
                    "alternates": [
                        {
                            "href": "/atom.xml",
                            "type": "application/atom+xml",
                            "title": "Atom feed",
                        }
                    ]
                },
            )

        response = LinkHeaderMiddleware(get_response)(request)

        assert response.headers["Link"] == (
            '</sitemap.xml>; rel="sitemap"; type="application/xml", '
            '</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json", '
            '</atom.xml>; rel="alternate"; type="application/atom+xml"; title="Atom feed"'
        )

    def test_leaves_non_template_responses_with_sitewide_links(self):
        request = self.request_factory.get("/robots.txt")

        def get_response(_request):
            return HttpResponse("ok")

        response = LinkHeaderMiddleware(get_response)(request)

        assert response.headers["Link"] == (
            '</sitemap.xml>; rel="sitemap"; type="application/xml", '
            '</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json"'
        )

    def test_skips_temporary_and_permanent_redirects(self):
        request = self.request_factory.get("/old-path")

        for redirect_response in (
            HttpResponseRedirect("/new-path"),
            HttpResponsePermanentRedirect("/new-path"),
        ):

            def get_response(_request, response=redirect_response):
                return response

            response = LinkHeaderMiddleware(get_response)(request)

            assert "Link" not in response.headers

    def test_response_link_headers_attribute_works_on_any_response_type(self):
        request = self.request_factory.get("/ewca/civ/2024/1/data.xml")

        def get_response(_request):
            response = HttpResponse("<xml/>", content_type="application/xml")
            response.link_headers = [  # type: ignore[attr-defined]
                {"href": "/ewca/civ/2024/1", "rel": "alternate", "type": "text/html"},
            ]
            return response

        response = LinkHeaderMiddleware(get_response)(request)

        assert response.headers["Link"] == (
            '</sitemap.xml>; rel="sitemap"; type="application/xml", '
            '</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json", '
            '</ewca/civ/2024/1>; rel="alternate"; type="text/html"'
        )
