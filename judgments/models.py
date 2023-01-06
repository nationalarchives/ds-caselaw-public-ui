# from django.db import models
from collections.abc import Iterable
from os.path import dirname, join

from caselawclient.Client import api_client
from django.db import models
from djxml import xmlmodels
from ds_caselaw_utils.courts import Court as UtilsCourt
from ds_caselaw_utils.courts import CourtGroup as UtilsCourtGroup
from ds_caselaw_utils.courts import courts as utils_courts
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


class CourtDates(models.Model):
    param = models.CharField(max_length=64, primary_key=True)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(blank=False)


class CourtDecoratedWithDates:
    """
    This wraps the Court object from ds_caselaw_utils, checking in the db for
    up-to-date court date range information, and falling back to the hardcoded
    value if none is found.
    """

    def __init__(self, court_meta):
        self.code = court_meta.code
        self.name = court_meta.name
        self.list_name = court_meta.list_name
        self.link = court_meta.link
        self.ncn = court_meta.ncn
        self.canonical_param = court_meta.canonical_param
        self.param_aliases = court_meta.param_aliases
        try:
            dbdate = CourtDates.objects.get(pk=self.canonical_param)
            self.start_year = dbdate.start_year
            self.end_year = dbdate.end_year
        except CourtDates.DoesNotExist:
            self.start_year = court_meta.start_year
            self.end_year = court_meta.end_year


class CourtGroupDecoratedWithDates:
    """
    This wraps the CourtGroup object from ds_caselaw_utils, delegating each court
    to a decorated object which pulls dates from the db.
    """

    def __init__(self, group_meta):
        self.name = group_meta.name
        self.courts = [
            CourtDecoratedWithDates(court_meta) for court_meta in group_meta.courts
        ]


class CourtsRepositoryDecoratedWithDates:
    """
    This wraps the CourtsRepository object from ds_caselaw_utils, decorating the
    returned data with the database date.
    """

    def __decorate(self, data):
        if type(data) is UtilsCourt:
            return CourtDecoratedWithDates(data)
        elif type(data) is UtilsCourtGroup:
            return CourtGroupDecoratedWithDates(data)
        elif isinstance(data, Iterable):
            return [self.__decorate(d) for d in data]
        else:
            return data

    def __init__(self, repo):
        self.repo = repo

    def get_by_param(self, param):
        return self.__decorate(self.repo.get_by_param(param))

    def get_all(self):
        return self.__decorate(self.repo.get_all())

    def get_selectable(self):
        return self.__decorate(self.repo.get_selectable())

    def get_listable_groups(self):
        return self.__decorate(self.repo.get_listable_groups())

    def get_listable_courts(self):
        return self.__decorate(self.repo.get_listable_courts())

    def get_listable_tribunals(self):
        return self.__decorate(self.repo.get_listable_tribunals())


courts = CourtsRepositoryDecoratedWithDates(utils_courts)
