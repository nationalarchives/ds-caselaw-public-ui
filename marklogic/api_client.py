import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from django.conf import settings
from lxml import etree
from lxml.etree import Element
from requests.auth import HTTPBasicAuth

from config.settings.base import env

RESULTS_PER_PAGE = 10


class MarklogicAPIError(requests.HTTPError):
    pass


class MarklogicBadRequestError(MarklogicAPIError):
    pass


class MarklogicUnauthorizedError(MarklogicAPIError):
    pass


class MarklogicNotPermittedError(MarklogicAPIError):
    pass


class MarklogicResourceNotFoundError(MarklogicAPIError):
    pass


class MarklogicCommunicationError(MarklogicAPIError):
    pass


class MarklogicApiClient:

    http_error_classes = {
        400: MarklogicBadRequestError,
        401: MarklogicUnauthorizedError,
        403: MarklogicNotPermittedError,
        404: MarklogicResourceNotFoundError,
    }
    default_http_error_class = MarklogicCommunicationError

    def __init__(self, host: str, username: str, password: str, use_https: bool):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"{'https' if use_https else 'http'}://{self.host}:8011"
        # Apply auth / common headers to the session
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)

    def _path_to_request_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _raise_for_status(cls, response: requests.Response) -> None:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            new_error_class = cls.http_error_classes.get(
                status_code, cls.default_http_error_class
            )
            try:
                response_body = json.dumps(response.json(), indent=4)
            except requests.JSONDecodeError:
                response_body = response.content
            new_exception = new_error_class(
                "{}. Response body:\n{}".format(e, response_body)
            )
            new_exception.response = response
            raise new_exception

    def prepare_request_kwargs(
        self, method: str, path: str, body=None, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        kwargs = dict(url=self._path_to_request_url(path))
        if data is not None:
            data = {k: v for k, v in data.items() if v is not None}
            if method == "GET":
                kwargs["params"] = data
            else:
                kwargs["data"] = json.dumps(data)
        if body is not None:
            kwargs["data"] = body
        return kwargs

    def make_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, Any],
        body: str = None,
        data: Dict[str, Any] = None,
    ) -> requests.Response:
        kwargs = self.prepare_request_kwargs(method, path, body, data)
        self.session.headers = headers
        response = self.session.request(method, **kwargs)
        # Raise relevant exception for an erroneous response
        self._raise_for_status(response)
        return response

    def GET(self, path: str, headers: Dict[str, Any], **data: Any) -> requests.Response:
        return self.make_request("GET", path, headers, data)

    def POST(
        self, path: str, headers: Dict[str, Any], **data: Any
    ) -> requests.Response:
        return self.make_request("POST", path, headers, data)

    def get_judgment_xml(self, uri: str) -> str:
        headers = {"Accept": "text/xml"}
        return self.GET(f"LATEST/documents/?uri=/{uri.lstrip('/')}.xml", headers).text

    def get_judgments_index(self, page: str) -> requests.Response:
        start = (int(page) - 1) * RESULTS_PER_PAGE + 1
        headers = {"Accept": "multipart/mixed"}
        return self.GET(
            f"LATEST/search/?view=results&start={start}&pageLength={RESULTS_PER_PAGE}",
            headers,
        )

    def save_judgment_xml(self, uri: str, judgment_xml: Element) -> requests.Response:
        xml = etree.tostring(judgment_xml)
        headers = {"Accept": "text/xml", "Content-type": "application/xml"}
        return self.make_request(
            "PUT",
            f"LATEST/documents?uri=/{uri.lstrip('/')}.xml",
            headers=headers,
            body=xml,
        )

    def search_judgments(self, query: str, page: str) -> requests.Response:
        start = (int(page) - 1) * RESULTS_PER_PAGE + 1
        headers = {"Accept": "text/xml"}
        return self.GET(
            f"LATEST/search/?start={start}&q={query}&pageLength={RESULTS_PER_PAGE}",
            headers,
        )

    def list_judgments(self, court: str = None, page: str = "1") -> requests.Response:
        start = (int(page) - 1) * RESULTS_PER_PAGE + 1
        headers = {"Accept": "text/xml"}

        query = f"court:{court}" if court else ""
        return self.GET(
            f"LATEST/search/?start={start}&q={query}&pageLength={RESULTS_PER_PAGE}",
            headers,
        )


class MockAPIClient:

    fixtures_dir: str = settings.MARKLOGIC_FIXTURES_DIR

    def get_judgment_xml(self, uri: str) -> str:
        filepath = os.path.join(self.fixtures_dir, uri.lstrip("/") + ".xml")

        try:
            return Path(filepath).read_text()
        except FileNotFoundError:
            raise MarklogicResourceNotFoundError

    def get_judgments_index(self, page: int) -> str:
        filepath = os.path.join(
            self.fixtures_dir, "search", "results" + str(page) + ".xml"
        )
        try:
            return Path(filepath).read_text()
        except FileNotFoundError:
            raise MarklogicResourceNotFoundError

    def search_judgments(self, query: str, page: str):
        filepath = os.path.join(
            self.fixtures_dir, "search", "results" + str(page) + ".xml"
        )
        try:
            return Path(filepath).read_text()
        except FileNotFoundError:
            raise MarklogicResourceNotFoundError


if env.bool("MARKLOGIC_MOCK_REQUESTS", default=False):
    api_client = MockAPIClient()
else:
    api_client = MarklogicApiClient(
        host=env("MARKLOGIC_HOST"),
        username=env("MARKLOGIC_USER"),
        password=env("MARKLOGIC_PASSWORD"),
        use_https=env("MARKLOGIC_USE_HTTPS", default=False),
    )
