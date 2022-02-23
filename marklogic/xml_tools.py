from xml.etree.ElementTree import Element

from lxml import etree

akn_namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
search_namespace = {"search": "http://marklogic.com/appservices/search"}


class JudgmentMissingMetadataError(IndexError):
    pass


def get_metadata_name_value(xml) -> str:
    try:
        name = xml.xpath(
            "//akn:FRBRname/@value",
            namespaces=akn_namespace,
        )[0]
    except IndexError:
        raise JudgmentMissingMetadataError
    return name


def get_metadata_name_element(xml) -> Element:
    try:
        name = xml.xpath(
            "//akn:FRBRname",
            namespaces=akn_namespace,
        )[0]
    except IndexError:
        raise JudgmentMissingMetadataError
    return name


def get_search_matches(element) -> [str]:
    nodes = element.xpath("//search:match", namespaces=search_namespace)
    results = []
    for node in nodes:
        text = etree.tostring(node, method="text", encoding="UTF-8")
        results.append(text.decode("UTF-8").strip())
    return results
