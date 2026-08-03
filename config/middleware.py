from typing import TypedDict
from urllib.parse import urlencode

from django.http.response import HttpResponseRedirectBase
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.cache import patch_cache_control
from typing_extensions import NotRequired


class _LinkHeader(TypedDict):
    href: str
    rel: str
    type: NotRequired[str]
    title: NotRequired[str]


class RobotsTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        # If the response is a redirect, short-circuit adding the X-Robots-Tag
        if isinstance(response, HttpResponseRedirectBase):
            return response

        # If page_allow_index is True, short-circuit adding the X-Robots-Tag
        context_data = response.context_data if isinstance(response, TemplateResponse) else None
        if context_data and context_data.get("page_allow_index", False):
            return response

        # In all other cases, assume we don't want it indexing and add the noindex X-Robots-Tag.
        response.headers["X-Robots-Tag"] = "noindex,nofollow,noai"
        return response


class CacheHeaderMiddleware:
    # via https://docs.djangoproject.com/en/4.1/topics/http/middleware/

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        patch_cache_control(response, max_age=15 * 60, public=True)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class LinkHeaderMiddleware:
    SITEMAP_TYPE = "application/xml"
    API_CATALOG_TYPE = "application/linkset+json"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, HttpResponseRedirectBase):
            return response

        link_values = [self._serialise_link(link) for link in self._base_links()]

        # Per-resource links set explicitly by the view on the response object.
        # Works for any response type: HttpResponse, JsonResponse, TemplateResponse, etc.
        link_values.extend(self._serialise_link(link) for link in getattr(response, "link_headers", []))

        if isinstance(response, TemplateResponse):
            link_values.extend(self._serialise_link(link) for link in self._context_links(response))

        existing_link_header = response.headers.get("Link")
        if existing_link_header:
            link_values.insert(0, existing_link_header)

        response.headers["Link"] = ", ".join(link_values)
        return response

    def _base_links(self) -> list[_LinkHeader]:
        return [
            {"href": reverse("sitemap_index"), "rel": "sitemap", "type": self.SITEMAP_TYPE},
            {
                "href": reverse("api_catalog"),
                "rel": "api-catalog",
                "type": self.API_CATALOG_TYPE,
            },
        ]

    @staticmethod
    def _context_links(response: TemplateResponse) -> list[_LinkHeader]:
        context_data = response.context_data or {}
        links: list[_LinkHeader] = list(context_data.get("links", []))
        for alternate in context_data.get("alternates", []):
            link: _LinkHeader = {"href": alternate["href"], "rel": "alternate"}
            if alternate.get("type"):
                link["type"] = alternate["type"]
            if alternate.get("title"):
                link["title"] = alternate["title"]
            links.append(link)
        return links

    @staticmethod
    def _serialise_link(link: _LinkHeader) -> str:
        segments = [f"<{link['href']}>", f'rel="{link["rel"]}"']
        if link.get("type"):
            segments.append(f'type="{link["type"]}"')
        if link.get("title"):
            segments.append(f'title="{link["title"]}"')
        return "; ".join(segments)


class LicensingEmailAddressMiddleware:
    EMAIL_ADDRESS = "caselawlicence@nationalarchives.gov.uk"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data["licensing_email_address"] = self.EMAIL_ADDRESS

        return response


class FeedbackLinkMiddleware:
    BASE_FEEDBACK_URL: str = "https://www.smartsurvey.co.uk/s/findcaselaw-feedback/"
    RECRUITMENT_URL: str = "https://www.smartsurvey.co.uk/s/tna_bulk_access/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We don't manipulate the response here
        return self.get_response(request)

    def process_template_response(self, request, response):
        params = {
            "full_url": request.build_absolute_uri(),
        }

        if "query" in response.context_data:
            params["search_term"] = response.context_data["query"]

        if "feedback_survey_type" in response.context_data:
            params["type"] = response.context_data["feedback_survey_type"]

        if "feedback_survey_document_uri" in response.context_data:
            # TODO: update the survey to allow for generalisation to `document`
            # https://trello.com/c/l0iBFM1e/1151-update-survey-to-account-for-judgment-the-fact-that-we-have-press-summaries-as-well-as-judgments-now
            params["judgment_uri"] = response.context_data["feedback_survey_document_uri"]

        if "feedback_survey_court" in response.context_data:
            params["court"] = response.context_data["feedback_survey_court"]

        if "feedback_survey_tribunal" in response.context_data:
            params["tribunal"] = response.context_data["feedback_survey_tribunal"]

        response.context_data["feedback_survey_link"] = self.BASE_FEEDBACK_URL + "?" + urlencode(params)
        response.context_data["recruitment_survey_link"] = self.RECRUITMENT_URL + "?" + urlencode(params)
        return response


class StructuredBreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        if "breadcrumbs" in response.context_data:
            response.context_data["structured_breadcrumbs"] = [
                {"text": "Find Case Law", "url": request.build_absolute_uri(reverse("home"))}
            ]
            for breadcrumb in response.context_data["breadcrumbs"]:
                response.context_data["structured_breadcrumbs"].append(
                    {
                        "text": breadcrumb["text"],
                        "url": request.build_absolute_uri(breadcrumb["url"]) if "url" in breadcrumb else None,
                    }
                )

        return response
