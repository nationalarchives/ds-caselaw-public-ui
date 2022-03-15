import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart import decoder

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

    def get_judgment_xml(self, judgment_uri, show_unpublished=False) -> str:
        uri = f"/{judgment_uri.lstrip('/')}.xml"
        xquery_path = os.path.join(
            settings.ROOT_DIR, "judgments", "xquery", "get_judgment.xqy"
        )

        response = self.eval(
            xquery_path,
            vars=f'{{"uri":"{uri}", "show_unpublished":{str(show_unpublished).lower()}}}',
            accept_header="application/xml",
        )
        multipart_data = decoder.MultipartDecoder.from_response(response)
        return multipart_data.parts[0].text

    def get_judgment_name(self, judgment_uri) -> str:
        uri = f"/{judgment_uri.lstrip('/')}.xml"
        xquery_path = os.path.join(
            settings.ROOT_DIR, "judgments", "xquery", "get_metadata_name.xqy"
        )

        response = self.eval(
            xquery_path, vars=f'{{"uri":"{uri}"}}', accept_header="application/xml"
        )
        multipart_data = decoder.MultipartDecoder.from_response(response)
        return multipart_data.parts[0].text

    def advanced_search(
        self,
        q=None,
        court=None,
        judge=None,
        party=None,
        order=None,
        date_from=None,
        date_to=None,
        page=1,
        show_unpublished=False,
    ) -> requests.Response:
        xquery_path = os.path.join(
            settings.ROOT_DIR, "judgments", "xquery", "advanced_search.xqy"
        )
        vars = f'{{"court":"{str(court or "")}","judge":"{str(judge or "")}",\
        "page":{page},"page-size":{RESULTS_PER_PAGE},"q":"{str(q or "")}","party":"{str(party or "")}",\
        "order":"{str(order or "")}","from":"{str(date_from or "")}","to":"{str(date_to or "")}",\
        "show_unpublished":{str(show_unpublished).lower()}}}'

        return self.eval(xquery_path, vars)

    def eval_xslt(self, judgment_uri) -> requests.Response:
        uri = f"/{judgment_uri.lstrip('/')}.xml"
        xquery_path = os.path.join(
            settings.ROOT_DIR, "judgments", "xquery", "xslt_transform.xqy"
        )

        return self.eval(
            xquery_path, vars=f'{{"uri":"{uri}"}}', accept_header="application/xml"
        )

    def eval(
        self, xquery_path, vars, database="Judgments", accept_header="multipart/mixed"
    ):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": accept_header,
        }
        data = {
            "xquery": Path(xquery_path).read_text(),
            "vars": vars,
        }
        path = f"LATEST/eval?database={database}"
        response = self.session.request(
            "POST", url=self._path_to_request_url(path), headers=headers, data=data
        )
        # Raise relevant exception for an erroneous response
        self._raise_for_status(response)
        return response


api_client = MarklogicApiClient(
    host=env("MARKLOGIC_HOST"),
    username=env("MARKLOGIC_USER"),
    password=env("MARKLOGIC_PASSWORD"),
    use_https=env("MARKLOGIC_USE_HTTPS", default=False),
)
