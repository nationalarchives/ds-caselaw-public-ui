from functools import cached_property
from typing import Optional, Union, cast

from caselawclient.models.documents import Document, DocumentURIString
from caselawclient.models.judgments import Judgment
from caselawclient.models.press_summaries import PressSummary
from django.template.defaultfilters import filesizeformat

from judgments.models.document_pdf import DocumentPdf
from judgments.utils import preprocess_query


class DocumentPresenter:
    MOST_RECENT_VERSION = DocumentURIString("")
    PASSTHROUGH_PROPERTIES = [
        "uri",
        "document_noun",
        "name",
        "content_as_xml",
    ]
    PASSTHROUGH_ALIASES = {
        "judgment_ncn": "best_human_identifier",
        "document_uri": "uri",
        "page_title": "name",
    }

    def __init__(self, doc: Document, pdf: DocumentPdf, query: Optional[str] = None):
        self.doc: Union[PressSummary, Judgment]
        if doc.document_noun == "press summary":
            self.doc = cast(PressSummary, doc)
        else:
            self.doc = cast(Judgment, doc)
        self.query = query
        self.pdf = pdf

    def __getattr__(self, name):
        if name in self.PASSTHROUGH_PROPERTIES:
            return getattr(self.doc, name)
        elif name in self.PASSTHROUGH_ALIASES.keys():
            return getattr(self.doc, self.PASSTHROUGH_ALIASES[name])
        else:
            raise AttributeError(name)

    @cached_property
    def number_of_mentions(self):
        if self.query:
            return self.doc.number_of_mentions(self.query)

    @cached_property
    def linked_document_uri(self):
        return self.linked_document.uri

    @cached_property
    def linked_document(self):
        return self.doc.linked_document

    @cached_property
    def content(self):
        return self.doc.content_as_html(
            self.MOST_RECENT_VERSION,
            query=preprocess_query(self.query) if self.query is not None else None,
        )

    @cached_property
    def pdf_size(self):
        """Return the size of the S3 PDF for a document as a string in brackets, or an empty string if unavailable"""
        size = self.pdf.size
        if size is None:
            return ""
        else:
            return f" ({filesizeformat(size)})"

    @cached_property
    def pdf_uri(self):
        return self.pdf.uri

    @property
    def breadcrumbs(self):
        if self.doc.document_noun == "press summary":
            return [
                {
                    "url": "/" + self.linked_document_uri,
                    "text": self.linked_document.name,
                },
                {
                    "text": "Press Summary",
                },
            ]
        else:
            return [
                {"text": self.name},
            ]
