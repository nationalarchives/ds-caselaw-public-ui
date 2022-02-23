from unittest import skip

from django.test import TestCase

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
                            <FRBRname value="My Judgment Name"/>
                        </identification>
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
        self.assertEqual("My Judgment Name", model.metadata_name.get("value"))
        self.assertEqual("[2017] EWHC 3289 (QB)", model.neutral_citation)
