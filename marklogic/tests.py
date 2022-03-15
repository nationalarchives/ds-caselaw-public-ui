from django.test import TestCase
from lxml import etree

from marklogic import xml_tools
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

    def test_search_matches(self):
        xml_string = """
            <search:result index="11" xmlns:search="http://marklogic.com/appservices/search"
                uri="/ewhc/admin/2013/2575.xml"
                path="fn:doc('/ewhc/admin/2013/2575.xml')"
                href="/v1/documents?uri=%2Fewhc%2Fadmin%2F2013%2F2575.xml"
                mimetype="application/xml"
                format="xml">
                <search:snippet>
                    <search:match
                        path="fn:doc('/ewhc/admin/2013/2575.xml')/*:akomaNtoso/*:judgment/*:header/*:p[9]/*:span">
                        HH <search:highlight>Judge</search:highlight> Anthony Thornton QC
                    </search:match>
                </search:snippet>
            </search:result>
        """
        xml = etree.fromstring(xml_string)
        result = xml_tools.get_search_matches(xml)
        self.assertEqual(result, ["HH Judge Anthony Thornton QC"])
