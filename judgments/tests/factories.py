import uuid

from caselawclient.identifier_resolution import IdentifierResolution, IdentifierResolutions
from caselawclient.models.documents import DocumentURIString
from caselawclient.xquery_type_dicts import MarkLogicDocumentURIString
from factory.django import DjangoModelFactory

from judgments.models import CourtDates


class CourtDateFactory(DjangoModelFactory):
    class Meta:
        model = CourtDates

    param = "uksc"
    start_year = 2001
    end_year = 2024


class IdentifierResolutionsFactory:
    @classmethod
    def build(cls, identifier_uuid=None, uri="/ml_example_url.xml", slug="uksc/1979/999") -> IdentifierResolutions:
        if not identifier_uuid:
            identifier_uuid = str(uuid.uuid4())
        return IdentifierResolutions(
            [
                IdentifierResolution(
                    identifier_uuid=f"id-{uuid}",
                    document_uri=MarkLogicDocumentURIString(uri),
                    identifier_slug=DocumentURIString(slug),
                    document_published=True,
                )
            ]
        )
