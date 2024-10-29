import logging
from functools import cached_property

import environ
import requests
from caselawclient.models.documents import DocumentURIString

from judgments.utils import formatted_document_uri


class DocumentPdf:
    def __init__(self, document_uri: DocumentURIString):
        self.document_uri: DocumentURIString = document_uri

    @cached_property
    def size(self):
        """Return the size of the S3 PDF for a document, or None if unavailable"""
        response = requests.head(
            # it is possible that "" is a better value than None, but that is untested
            self.generate_uri(),
            headers={"Accept-Encoding": None},
        )
        content_length = response.headers.get("Content-Length", None)
        if response.status_code >= 400:
            return None
        if content_length:
            return int(content_length)
        else:
            logging.warning(f"Unable to determine PDF size for {self.document_uri}")
            return None

    @cached_property
    def uri(self) -> str:
        return self.generate_uri() if self.size else formatted_document_uri(self.document_uri, "pdf")

    def generate_uri(self):
        env = environ.Env()
        """Create a string saying where the S3 PDF will be for a judgment uri"""
        pdf_path = f'{self.document_uri}/{self.document_uri.replace("/", "_")}.pdf'
        assets = env("ASSETS_CDN_BASE_URL", default=None)
        if assets:
            return f"{assets}/{pdf_path}"
        else:
            return f'https://{env("PUBLIC_ASSET_BUCKET")}.s3.{env("S3_REGION")}.amazonaws.com/{pdf_path}'
