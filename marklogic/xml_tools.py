from xml.etree.ElementTree import Element

akn_namespace = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}


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


def get_neutral_citation(xml) -> str:
    try:
        neutral_citation = xml.xpath(
            "//akn:neutralCitation",
            namespaces=akn_namespace,
        )[0].text
    except IndexError:
        raise JudgmentMissingMetadataError
    return neutral_citation
