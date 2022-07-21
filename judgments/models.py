# from django.db import models
from os.path import dirname, join

from caselawclient.Client import api_client
from djxml import xmlmodels
from lxml import etree


class Judgment(xmlmodels.XmlModel):
    class Meta:
        namespaces = {
            "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "uk": "https://caselaw.nationalarchives.gov.uk/akn",
        }

    metadata_name = xmlmodels.XPathTextField(
        "//akn:FRBRname/@value", ignore_extra_nodes=True
    )
    neutral_citation = xmlmodels.XPathTextField(
        "//akn:proprietary/uk:cite", ignore_extra_nodes=True
    )
    date = xmlmodels.XPathTextField(
        "//akn:FRBRdate[@name='judgment']/@date", ignore_extra_nodes=True
    )
    court = xmlmodels.XPathTextField("//akn:proprietary/uk:court")
    content_hash = xmlmodels.XPathTextField("//akn:proprietary/uk:hash")


class SearchResult:
    def __init__(
        self,
        uri="",
        neutral_citation="",
        name="",
        court="",
        date="",
        matches=[],
        author="",
        last_modified="",
        content_hash="",
    ) -> None:
        self.uri = uri
        self.neutral_citation = neutral_citation
        self.name = name
        self.date = date
        self.court = court
        self.matches = matches
        self.author = author
        self.last_modified = last_modified
        self.content_hash = content_hash

    @staticmethod
    def create_from_node(node):
        uri = node.xpath("@uri")[0].lstrip("/").split(".xml")[0]
        matches = SearchMatch.create_from_string(
            etree.tostring(node, encoding="UTF-8").decode("UTF-8")
        )
        judgment_xml = api_client.get_judgment_xml(uri)
        judgment = Judgment.create_from_string(judgment_xml)

        author = api_client.get_property(uri, "source-organisation")
        last_modified = api_client.get_last_modified(uri)

        if len(str(matches.transform_to_html())) == 0:
            matches = None
        else:
            matches = matches.transform_to_html()

        return SearchResult(
            uri=uri,
            neutral_citation=judgment.neutral_citation,
            name=judgment.metadata_name,
            matches=matches,
            court=judgment.court,
            date=judgment.date,
            author=author,
            last_modified=last_modified,
            content_hash=judgment.content_hash,
        )


class SearchResults(xmlmodels.XmlModel):
    class Meta:
        namespaces = {"search": "http://marklogic.com/appservices/search"}

    total = xmlmodels.XPathTextField("//search:response/@total")
    results = xmlmodels.XPathListField("//search:response/search:result")


class SearchMatch(xmlmodels.XmlModel):
    class Meta:
        namespaces = {"search": "http://marklogic.com/appservices/search"}

    transform_to_html = xmlmodels.XsltField(join(dirname(__file__), "search_match.xsl"))
