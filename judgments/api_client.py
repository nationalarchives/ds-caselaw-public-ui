import requests
from requests.auth import HTTPBasicAuth

from config.settings.base import env


class MockResponse:
    def __init__(self, xml_data, status_code):
        self.xml_data = xml_data
        self.status_code = status_code

    def text(self):
        return self.xml_data

    def status_code(self):
        return self.status_code


class ApiClient:
    def get(judgment_uri):
        if env("USE_MARKLOGIC") == "True":
            url = (
                "http://"
                + env("MARKLOGIC_HOST")
                + ":8011/LATEST/documents/?uri=/"
                + judgment_uri
                + ".xml"
            )
            return requests.get(
                url,
                auth=HTTPBasicAuth(env("MARKLOGIC_USER"), env("MARKLOGIC_PASSWORD")),
            )
        else:
            file_path = "./judgments/data/" + judgment_uri + ".xml"
            try:
                file = open(file_path)
                return MockResponse(file.read(), 200)
            except FileNotFoundError:
                return MockResponse("File not found", 404)
