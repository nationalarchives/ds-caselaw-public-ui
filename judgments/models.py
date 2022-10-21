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
        "/akn:akomaNtoso/akn:judgment/akn:meta/akn:identification/akn:FRBRWork/"
        + "akn:FRBRname/@value",
        ignore_extra_nodes=True,
    )
    neutral_citation = xmlmodels.XPathTextField(
        "//akn:proprietary/uk:cite", ignore_extra_nodes=True
    )
    date = xmlmodels.XPathTextField(
        "/akn:akomaNtoso/akn:judgment/akn:meta/akn:identification/akn:FRBRWork/"
        + "akn:FRBRdate/@date",
        ignore_extra_nodes=True,
    )
    court = xmlmodels.XPathTextField("//akn:proprietary/uk:court")
    content_hash = xmlmodels.XPathTextField("//akn:proprietary/uk:hash")
    transformation_date = xmlmodels.XPathTextField(
        "/akn:akomaNtoso/akn:judgment/akn:meta/akn:identification/akn:FRBRManifestation/"
        + "akn:FRBRdate[@name='transform']/@date"
    )


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
        transformation_date="",
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
        self.transformation_date = transformation_date

    @staticmethod
    def create_from_node(node):
        uri = node.xpath("@uri")[0].lstrip("/").split(".xml")[0]
        matches = SearchMatch.create_from_string(
            etree.tostring(node, encoding="UTF-8").decode("UTF-8")
        )
        namespaces = {
            "search": "http://marklogic.com/appservices/search",
            "uk": "https://caselaw.nationalarchives.gov.uk/akn",
            "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        }
        neutral_citation = (
            node.xpath("search:extracted/uk:cite", namespaces=namespaces)[0].text
            if node.xpath("search:extracted/uk:cite", namespaces=namespaces)
            else ""
        )
        court = (
            node.xpath("search:extracted/uk:court", namespaces=namespaces)[0].text
            if node.xpath("search:extracted/uk:court", namespaces=namespaces)
            else ""
        )
        metadata_name = (
            node.xpath("search:extracted/akn:FRBRname/@value", namespaces=namespaces)[0]
            if node.xpath("search:extracted/akn:FRBRname/@value", namespaces=namespaces)
            else ""
        )
        date = (
            node.xpath(
                "search:extracted/akn:FRBRdate[(@name='judgment' or @name='decision')]/@date",
                namespaces=namespaces,
            )[0]
            if node.xpath(
                "search:extracted/akn:FRBRdate[(@name='judgment' or @name='decision')]/@date",
                namespaces=namespaces,
            )
            else ""
        )
        transformation_date = (
            node.xpath(
                "search:extracted/akn:FRBRdate[@name='transform']/@date",
                namespaces=namespaces,
            )[0]
            if node.xpath(
                "search:extracted/akn:FRBRdate[@name='transform']/@date",
                namespaces=namespaces,
            )
            else ""
        )
        content_hash = (
            node.xpath("search:extracted/uk:hash", namespaces=namespaces)[0].text
            if node.xpath("search:extracted/uk:hash", namespaces=namespaces)
            else ""
        )
        author = api_client.get_property(uri, "source-organisation")
        last_modified = api_client.get_last_modified(uri)

        if len(str(matches.transform_to_html())) == 0:
            matches = None
        else:
            matches = matches.transform_to_html()

        return SearchResult(
            uri=uri,
            neutral_citation=neutral_citation,
            name=metadata_name,
            matches=matches,
            court=court,
            date=date,
            author=author,
            last_modified=last_modified,
            content_hash=content_hash,
            transformation_date=transformation_date,
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
