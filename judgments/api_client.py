import requests
from requests.auth import HTTPBasicAuth

from config.settings.base import env


class ApiClient:
    def get(judgment_uri):
        url = (
            "http://"
            + env("MARKLOGIC_HOST")
            + ":8011/LATEST/documents/?uri=/"
            + judgment_uri
            + ".xml"
        )
        return requests.get(url, auth=HTTPBasicAuth("admin", "admin"))
