import logging
from abc import ABC, abstractmethod
from functools import cached_property

import environ
import requests
from caselawclient.models.documents import DocumentURIString

from judgments.utils import formatted_document_uri


class DocumentDownload(ABC):
    @property
    @abstractmethod
    def document_type_string(self) -> str:
        """What sort of document this is, for inserting into user/developer facing messages"""
        pass

    @property
    @abstractmethod
    def document_extension(self) -> str:
        """The extension of the document, with no dot prefix"""
        pass

    def __init__(self, document_uri: DocumentURIString):
        self.document_uri: DocumentURIString = document_uri

    @cached_property
    def size(self):
        """Return the size of the S3 download for a document, or None if unavailable"""
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
            logging.warning(f"Unable to determine {self.document_type_string} size for {self.document_uri}")
            return None

    @cached_property
    def uri(self) -> str:
        return self.generate_uri() if self.size else formatted_document_uri(self.document_uri, "pdf")

    def generate_uri(self):
        env = environ.Env()
        """Create a string saying where the S3 PDF will be for a judgment uri"""
        file_path = f"{self.document_uri}/{self.document_uri.replace('/', '_')}.{self.document_extension}"
        assets = env("ASSETS_CDN_BASE_URL", default=None)
        if assets:
            return f"{assets}/{file_path}"
        else:
            return f"https://{env('PUBLIC_ASSET_BUCKET')}.s3.{env('S3_REGION')}.amazonaws.com/{file_path}"


class DocumentPdf(DocumentDownload):
    @property
    def document_type_string(self):
        return "PDF"

    @property
    def document_extension(self):
        return "pdf"


class DocumentDocx(DocumentDownload):
    @property
    def document_type_string(self):
        return "Word document"

    @property
    def document_extension(self):
        return "docx"
