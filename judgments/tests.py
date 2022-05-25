import re
from unittest import skip

from django.test import TestCase

from judgments import converters, views
from judgments.models import Judgment


class TestAtomFeed(TestCase):
    def test_feed_exists(self):
        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")
        # that there is a valid page
        self.assertEqual(response.status_code, 200)
        # that it has the correct site name
        self.assertIn("<name>The National Archives</name>", decoded_response)
        # that it is like an Atom XML document
        self.assertIn("http://www.w3.org/2005/Atom", decoded_response)
        # that it has at least one entry
        self.assertIn("<entry>", decoded_response)


class TestJudgment(TestCase):
    @skip
    def test_valid_content(self):
        response = self.client.get("/judgments/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("[2004] EWCA Civ 632", decoded_response)
        self.assertEqual(response.status_code, 200)

    @skip
    def test_404_response(self):
        response = self.client.get("/judgments/ewca/civ/2004/63X")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("Judgment was not found", decoded_response)
        self.assertEqual(response.status_code, 404)


class TestJudgmentModel(TestCase):
    def test_can_parse_judgment(self):
        xml = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna">
                            <FRBRdate date="2004-06-10" name="judgment"/>
                            <FRBRname value="My Judgment Name"/>
                        </identification>
                        <proprietary source="ewca/civ/2004/811/eng/docx"
                            xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
                            <uk:court>EWCA-Civil</uk:court>
                            <uk:cite>[2017] EWHC 3289 (QB)</uk:cite>
                        </proprietary>
                    </meta>
                </judgment>
            </akomaNtoso>
        """

        model = Judgment.create_from_string(xml)
        self.assertEqual("My Judgment Name", model.metadata_name)
        self.assertEqual("[2017] EWHC 3289 (QB)", model.neutral_citation)
        self.assertEqual("2004-06-10", model.date)
        self.assertEqual("EWCA-Civil", model.court)


class TestPaginator(TestCase):
    def test_paginator(self):
        expected_result = {
            "current_page": 10,
            "has_next_page": True,
            "has_prev_page": True,
            "next_page": 11,
            "prev_page": 9,
            "next_pages": [11, 12, 13, 14, 15, 16, 17, 18, 19],
            "number_of_pages": 200,
        }
        self.assertEqual(views.paginator(10, 2000), expected_result)


class TestConverters(TestCase):
    def test_year_converter_parses_year(self):
        converter = converters.YearConverter()
        match = re.match(converter.regex, "1994")

        self.assertEqual(match.group(0), "1994")

    def test_year_converter_converts_to_python(self):
        converter = converters.YearConverter()
        self.assertEqual(converter.to_python("1994"), 1994)

    def test_year_converter_converts_to_url(self):
        converter = converters.YearConverter()
        self.assertEqual(converter.to_url(1994), "1994")

    def test_date_converter_parses_date(self):
        converter = converters.DateConverter()
        match = re.match(converter.regex, "2022-02-28")
        self.assertEqual(match.group(0), "2022-02-28")

    def test_date_converter_fails_to_parse_string(self):
        converter = converters.DateConverter()
        match = re.match(converter.regex, "202L-ab-er")
        self.assertIsNone(match)

    def test_court_converter_parses_court(self):
        converter = converters.CourtConverter()
        match = re.match(converter.regex, "ewhc")
        self.assertEqual(match.group(0), "ewhc")

    def test_court_converter_fails_to_parse(self):
        converter = converters.CourtConverter()
        self.assertIsNone(re.match(converter.regex, "notacourt"))

    def test_subdivision_converter_parses_court(self):
        converter = converters.SubdivisionConverter()
        match = re.match(converter.regex, "comm")
        self.assertEqual(match.group(0), "comm")

    def test_subdivision_converter_fails_to_parse(self):
        converter = converters.SubdivisionConverter()
        self.assertIsNone(re.match(converter.regex, "notasubdivision"))
