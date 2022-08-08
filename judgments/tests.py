import re
from unittest import skip
from unittest.mock import patch

from django.test import TestCase

import judgments.models
import judgments.utils  # noqa: F401 -- used to mock
from judgments import converters, views
from judgments.models import Judgment, SearchResult, SearchResults


def fake_search_results():
    with open("fixtures/search_results.xml", "r") as f:
        return SearchResults.create_from_string(f.read())


def fake_search_result():
    return SearchResult(
        uri="ewhc/ch/2022/1.xml",
        neutral_citation="[2022] EWHC 1 (Ch)",
        name="A SearchResult name!",
        matches=[],
        court="A court!",
        date="2022-01-01T00:01:00",
        author="",
        last_modified="2022-01-01T00:01:00.123",
        content_hash="A hash!",
        transformation_date="2022-01-01T00:02:00",
    )


class TestAtomFeed(TestCase):
    @patch("judgments.utils.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_feed_exists(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()

        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")
        # that there is a valid page
        self.assertEqual(response.status_code, 200)
        # that it has the correct site name
        self.assertIn("<name>The National Archives</name>", decoded_response)
        # that it is like an Atom XML document
        self.assertIn("http://www.w3.org/2005/Atom", decoded_response)
        # that it has an entry
        self.assertIn("<entry>", decoded_response)
        # and it contains actual content - neither neutral citation or court appear in the feed to test.
        self.assertIn("A SearchResult name!", decoded_response)

    @patch("judgments.utils.perform_advanced_search")
    def test_bad_page_404(self, fake_advanced_search):
        # "&page=" 404s, not 500
        fake_advanced_search.return_value = fake_search_results()
        response = self.client.get("/atom.xml&page=")
        self.assertEqual(response.status_code, 404)


class TestJudgment(TestCase):
    @patch("judgments.views.requests.head")
    @patch("judgments.views.Judgment")
    @patch("judgments.views.decoder.MultipartDecoder")
    @patch("judgments.views.api_client")
    def test_valid_content(self, client, decoder, judgment, head):
        head.return_value.headers = {"Content-Length": "1234567890"}
        client.eval_xslt.return_value = "eval_xslt"
        decoder.MultipartDecoder.from_response.return_value.parts[0].text = "part0text"
        judgment.create_from_string.return_value.metadata_name = "judgment metadata"

        response = self.client.get("/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("(1.1\xa0GB)", decoded_response)
        # We don't use the Download as PDF text because there's an issue with localisated strings on CI
        self.assertEqual(response.status_code, 200)

    @skip
    def test_good_response(self):
        response = self.client.get("/ewca/civ/2004/637")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("[2004] EWCA Civ 637", decoded_response)
        self.assertEqual(response.status_code, 200)

    @skip
    def test_404_response(self):
        response = self.client.get("/ewca/civ/2004/63X")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("Page not found", decoded_response)
        self.assertEqual(response.status_code, 404)


class TestJudgmentModel(TestCase):
    def test_can_parse_judgment(self):
        xml = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna">
                            <FRBRManifestation>
                                <FRBRname value="My Judgment Name"/>
                                <FRBRdate date="2020-01-01T10:30:00" name="transform"/>
                            </FRBRManifestation>
                            <FRBRWork>
                                <FRBRname value="My Judgment Name"/>
                                <FRBRdate date="2004-06-10T10:30:00" name="judgment"/>
                            </FRBRWork>
                        </identification>
                        <proprietary source="ewca/civ/2004/811/eng/docx"
                            xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
                            <uk:court>EWCA-Civil</uk:court>
                            <uk:cite>[2017] EWHC 3289 (QB)</uk:cite>
                            <uk:hash>A hash!</uk:hash>
                        </proprietary>
                    </meta>
                </judgment>
            </akomaNtoso>
        """

        model = Judgment.create_from_string(xml)
        self.assertEqual("My Judgment Name", model.metadata_name)
        self.assertEqual("[2017] EWHC 3289 (QB)", model.neutral_citation)
        self.assertEqual("2004-06-10T10:30:00", model.date)
        self.assertEqual("EWCA-Civil", model.court)
        self.assertEqual("2020-01-01T10:30:00", model.transformation_date)
        self.assertEqual("A hash!", model.content_hash)

    def test_can_parse_judgment_hearing_date(self):
        xml = """
            <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                <judgment name="judgment" contains="originalVersion">
                    <meta>
                        <identification source="#tna">
                            <FRBRManifestation>
                                <FRBRname value="My Judgment Name"/>
                                <FRBRdate date="2020-01-01T10:30:00" name="transform"/>
                            </FRBRManifestation>
                            <FRBRWork>
                                <FRBRname value="My Judgment Name"/>
                                <FRBRdate date="2004-06-10T10:30:00" name="hearing"/>
                            </FRBRWork>
                        </identification>
                        <proprietary source="ewca/civ/2004/811/eng/docx"
                            xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
                            <uk:court>EWCA-Civil</uk:court>
                            <uk:cite>[2017] EWHC 3289 (QB)</uk:cite>
                            <uk:hash>A hash!</uk:hash>
                        </proprietary>
                    </meta>
                </judgment>
            </akomaNtoso>
        """

        model = Judgment.create_from_string(xml)
        self.assertEqual("My Judgment Name", model.metadata_name)
        self.assertEqual("2004-06-10T10:30:00", model.date)


class TestPaginator(TestCase):
    def test_paginator_2500(self):
        expected_result = {
            "current_page": 10,
            "has_next_page": True,
            "has_prev_page": True,
            "next_page": 11,
            "prev_page": 9,
            "next_pages": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "number_of_pages": 250,
        }
        self.assertEqual(views.paginator(10, 2500), expected_result)

    def test_paginator_25(self):
        # 25 items has 5 items on page 3.
        expected_result = {
            "current_page": 1,
            "has_next_page": True,
            "has_prev_page": False,
            "next_page": 2,
            "prev_page": 0,
            "next_pages": [2, 3],
            "number_of_pages": 3,
        }
        self.assertEqual(views.paginator(1, 25), expected_result)

    def test_paginator_5(self):
        expected_result = {
            "current_page": 1,
            "has_next_page": False,
            "has_prev_page": False,
            "next_page": 2,  # Note: remember to check has_next_page
            "prev_page": 0,
            "next_pages": [],
            "number_of_pages": 1,
        }
        self.assertEqual(views.paginator(1, 5), expected_result)

    @skip("This test works locally but fails on CI, to fix")
    @patch("judgments.utils.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_pagination_links(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        response = self.client.get(
            "/judgments/advanced_search?court=ukut-iac&order=&page=3"
        )
        decoded_response = response.content.decode("utf-8")
        self.assertIn(
            "/judgments/advanced_search?court=ukut-iac&amp;order=&page=4",
            decoded_response,
        )


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
