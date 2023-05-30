import logging
from collections import defaultdict
from datetime import datetime
from os.path import dirname, join
from typing import Optional

from caselawclient.Client import api_client
from dateutil import parser as dateparser
from dateutil.parser import ParserError
from django.db import models
from django.db.models import Max, Min
from djxml import xmlmodels
from ds_caselaw_utils.courts import CourtNotFoundException, courts
from lxml import etree


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
        self.uri: str = uri.removesuffix(".xml")
        self.neutral_citation: str = neutral_citation
        self.name: str = name
        self.date: Optional[datetime]
        self.court: Optional[str]

        try:
            self.date = dateparser.parse(date)
        except ParserError as e:
            if date != "":
                logging.warning(
                    f'Unable to parse document date "{date}". Full error: {e}'
                )
            self.date = None
        try:
            self.court = courts.get_by_code(court)
        except CourtNotFoundException:
            self.court = None
        self.matches = matches
        self.author: Optional[str] = author
        self.last_modified = last_modified
        self.content_hash: str = content_hash
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


class CourtDates(models.Model):
    param = models.CharField(max_length=64, primary_key=True)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(blank=False)

    @staticmethod
    def min_year():
        result = CourtDates.objects.aggregate(Min("start_year"))
        return result["start_year__min"]

    @staticmethod
    def max_year():
        result = CourtDates.objects.aggregate(Max("end_year"))
        return result["end_year__max"]


class SearchFormErrors:
    def __init__(self):
        self.messages = []
        self.fields = defaultdict(list)

    def has_errors(self, field=None):
        if field is None:
            return len(self.messages) > 0 and len(self.fields.keys()) > 0
        else:
            return len(self.fields[field])

    def add_error(self, message, field=None, fieldMessage=None):
        self.messages.append(message)
        if field is not None:
            self.fields[field].append(fieldMessage)
