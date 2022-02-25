from unittest import skip

from django.test import TestCase

from judgments import views
from judgments.models import Judgment


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
                        <proprietary source="ewca/civ/2004/811/eng/docx" xmlns:uk="https:/judgments.gov.uk/">
                            <uk:court>EWCA-Civil</uk:court>
                        </proprietary>
                    </meta>
                    <header>
                        <p>
                            <neutralCitation>[2017] EWHC 3289 (QB)</neutralCitation>
                        </p>
                    </header>
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
