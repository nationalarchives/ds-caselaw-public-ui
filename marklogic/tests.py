from unittest.mock import MagicMock

from django.test import TestCase
from lxml import etree

from marklogic import xml_tools
from marklogic.api_client import MarklogicApiClient
from marklogic.xml_tools import JudgmentMissingMetadataError


class TestXmlTools(TestCase):
    def test_metadata_name_value_success(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna">
                            <FRBRname value="My Judgment Name"/>
                        </identification>
                    </meta>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        result = xml_tools.get_metadata_name_value(xml)
        self.assertEqual(result, "My Judgment Name")

    def test_metadata_name_value_failure(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna"/>
                    </meta>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        self.assertRaises(
            JudgmentMissingMetadataError, xml_tools.get_metadata_name_value, xml
        )

    def test_metadata_name_element_success(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna">
                            <FRBRname value="My Judgment Name"/>
                        </identification>
                    </meta>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        result = xml_tools.get_metadata_name_element(xml)
        self.assertEqual(
            result.tag, "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}FRBRname"
        )
        self.assertEqual(result.attrib, {"value": "My Judgment Name"})

    def test_metadata_name_element_failure(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna"/>
                    </meta>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        self.assertRaises(
            JudgmentMissingMetadataError, xml_tools.get_metadata_name_element, xml
        )

    def test_neutral_citation_success(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <header>
                        <neutralCitation>[2004] EWCA Civ 811</neutralCitation>
                    </header>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        result = xml_tools.get_neutral_citation(xml)
        self.assertEqual(result, "[2004] EWCA Civ 811")

    def test_neutral_citation_failure(self):
        xml_string = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <header/>
                </judgment>
            </akomaNtoso>
        """
        xml = etree.fromstring(xml_string)
        self.assertRaises(
            JudgmentMissingMetadataError, xml_tools.get_neutral_citation, xml
        )


class TestApiClient(TestCase):
    def test_get_judgment_xml(self):
        mock_api_client = MarklogicApiClient("a", "b", "c", True)
        mock_api_client.GET = MagicMock()
        uri = "/ewca/civ/2004/632"
        mock_api_client.get_judgment_xml(uri)
        mock_api_client.GET.assert_called_with(
            "LATEST/documents/?uri=/ewca/civ/2004/632.xml", {"Accept": "text/xml"}
        )

    def test_get_judgments_index(self):
        mock_api_client = MarklogicApiClient("a", "b", "c", True)
        mock_api_client.GET = MagicMock()
        mock_api_client.get_judgments_index("1")
        mock_api_client.GET.assert_called_with(
            "LATEST/search/?view=results&start=1", {"Accept": "multipart/mixed"}
        )

    def test_save_judgment_xml(self):
        mock_api_client = MarklogicApiClient("a", "b", "c", True)
        mock_api_client.make_request = MagicMock()
        uri = "/ewca/civ/2004/632"
        xml = etree.fromstring("<root></root>")
        mock_api_client.save_judgment_xml(uri, xml)
        mock_api_client.make_request.assert_called_with(
            "PUT",
            "LATEST/documents?uri=/ewca/civ/2004/632.xml",
            headers={"Accept": "text/xml", "Content-type": "application/xml"},
            body=b"<root/>",
        )
