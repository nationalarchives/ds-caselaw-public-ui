import pytest
from factories import JudgmentFactory


class TestJudgmentFactory:
    def test_default_uri(self):
        # The default URI gets a test where others don't because without a URI judgments fall apart
        judgment = JudgmentFactory.build()

        assert isinstance(judgment.uri, str)
        assert judgment.uri != ""

    @pytest.mark.parametrize(
        "parameter, value",
        [
            ("uri", "test/2022/321"),
            ("name", "Some Test Name"),
            ("neutral_citation", "[2022] Test 321"),
            ("court", "The Test Court"),
            ("judgment_date_as_string", "2022-03-04"),
            ("is_published", True),
            ("is_sensitive", True),
            ("is_anonymised", True),
            ("has_supplementary_materials", True),
            ("is_failure", True),
            ("source_name", "Uploader Test"),
            ("source_email", "test@example.com"),
            ("consignment_reference", "TDR-54321"),
            ("assigned_to", "Assignee"),
            ("versions", ["1", "2"]),
        ],
    )
    def test_params(self, parameter, value):
        judgment = JudgmentFactory.build(**{parameter: value})

        assert getattr(judgment, parameter) == value

    def test_html(self):
        judgment = JudgmentFactory.build(html="<h1>Testing HTML</h1>")

        assert judgment.content_as_html("") == "<h1>Testing HTML</h1>"

    def test_xml(self):
        judgment = JudgmentFactory.build(xml="<h1>Testing XML</h1>")

        assert judgment.content_as_xml == "<h1>Testing XML</h1>"
