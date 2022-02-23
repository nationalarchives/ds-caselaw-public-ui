# from django.db import models
from djxml import xmlmodels
from marklogic import xml_tools

class Judgment(xmlmodels.XmlModel):
    class Meta:
        namespaces = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}

    metadata_name = xmlmodels.XPathSingleNodeField("//akn:FRBRname")
    neutral_citation = xmlmodels.XPathTextField("//akn:neutralCitation", ignore_extra_nodes=True)


class SearchResult:
    uri = ""
    neutral_citation = ""
    name = ""
    matches = 0

    def __init__(self, uri = "", neutral_citation = "", name = "", matches = 0) -> None:
        self.uri = uri
        self.neutral_citation = neutral_citation
        self.name = name
        self.matches = matches

class SearchResults(xmlmodels.XmlModel):
    class Meta:
        extension_ns_uri = "urn:local:local_funcs"
        namespaces = {
            "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "search": "http://marklogic.com/appservices/search",
            "fn": extension_ns_uri
        }

    total = xmlmodels.XPathTextField("//search:response/@total")
    results = xmlmodels.XPathListField("//search:response/search:result")
