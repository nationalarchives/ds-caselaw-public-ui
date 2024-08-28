import re
from unittest.mock import patch

from django.test import TestCase
from factories import JudgmentFactory

from judgments import converters, utils
from judgments.models.court_dates import CourtDates
from judgments.tests.fixtures import FakeSearchResponse
from judgments.utils import clamp, paginator, search_context_from_url
from judgments.views.detail import PdfDetailView


class TestCourtDates(TestCase):
    def setUp(self):
        CourtDates.objects.create(param="earliest_starting_court", start_year=2001, end_year=2020)
        CourtDates.objects.create(param="last_ending_court", start_year=2005, end_year=2023)

    def test_min_year(self):
        self.assertEqual(CourtDates.min_year(), 2001)

    def test_max_year(self):
        self.assertEqual(CourtDates.max_year(), 2023)


class TestPaginator(TestCase):
    def test_paginator_2500(self):
        expected_result = {
            "show_first_page": True,
            "show_first_page_divider": True,
            "show_last_page": True,
            "show_last_page_divider": True,
            "current_page": 10,
            "has_next_page": True,
            "has_prev_page": True,
            "next_page": 11,
            "prev_page": 9,
            "page_range": [8, 9, 10, 11, 12],
            "number_of_pages": 250,
        }
        self.assertEqual(paginator(10, 2500), expected_result)

    def test_paginator_25(self):
        # 25 items has 5 items on page 3.
        expected_result = {
            "show_first_page": False,
            "show_first_page_divider": False,
            "show_last_page": False,
            "show_last_page_divider": False,
            "current_page": 1,
            "has_next_page": True,
            "has_prev_page": False,
            "next_page": 2,
            "prev_page": 0,
            "page_range": [1, 2, 3],
            "number_of_pages": 3,
        }
        self.assertEqual(paginator(1, 25), expected_result)

    def test_paginator_5(self):
        expected_result = {
            "show_first_page": False,
            "show_first_page_divider": False,
            "show_last_page": False,
            "show_last_page_divider": False,
            "current_page": 1,
            "has_next_page": False,
            "has_prev_page": False,
            "next_page": 2,  # Note: remember to check has_next_page
            "prev_page": 0,
            "page_range": [1],
            "number_of_pages": 1,
        }
        self.assertEqual(paginator(1, 5), expected_result)

    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_pagination_links(self, mock_search_judgments_and_parse_response):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?tribunal=ukut/iac&order=&page=3")
        decoded_response = response.content.decode("utf-8")
        self.assertIn(
            "/judgments/search?tribunal=ukut%2Fiac&amp;order=&page=4",
            decoded_response,
        )


class TestConverters(TestCase):
    def test_year_converter_parses_year(self):
        converter = converters.YearConverter()
        match = re.match(converter.regex, "1994")
        self.assertEqual(match.group(0), "1994")  # type: ignore

    def test_year_converter_converts_to_python(self):
        converter = converters.YearConverter()
        self.assertEqual(converter.to_python("1994"), 1994)

    def test_year_converter_converts_to_url(self):
        converter = converters.YearConverter()
        self.assertEqual(converter.to_url(1994), "1994")

    def test_date_converter_parses_date(self):
        converter = converters.DateConverter()
        match = re.match(converter.regex, "2022-02-28")
        self.assertEqual(match.group(0), "2022-02-28")  # type: ignore

    def test_date_converter_fails_to_parse_string(self):
        converter = converters.DateConverter()
        match = re.match(converter.regex, "202L-ab-er")
        self.assertIsNone(match)

    def test_court_converter_parses_court(self):
        converter = converters.CourtConverter()
        match = re.match(converter.regex, "ewhc")
        self.assertEqual(match.group(0), "ewhc")  # type: ignore

    def test_court_converter_fails_to_parse(self):
        converter = converters.CourtConverter()
        self.assertIsNone(re.match(converter.regex, "notacourt"))

    def test_subdivision_converter_parses_court(self):
        converter = converters.SubdivisionConverter()
        match = re.match(converter.regex, "comm")
        self.assertEqual(match.group(0), "comm")  # type:ignore

    def test_subdivision_converter_fails_to_parse(self):
        converter = converters.SubdivisionConverter()
        self.assertIsNone(re.match(converter.regex, "notasubdivision"))


class TestRobotsDirectives(TestCase):
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_homepage(self, mock_search_judgments_and_parse_response):
        # The homepage should not have a robots meta tag with nofollow,noindex
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/")
        self.assertNotContains(response, '<meta name="robots" content="noindex,nofollow" />')
        self.assertNotEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_search_results(self, mock_search_judgments_and_parse_response):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        # The judgment search results page should have a robots meta tag
        # with nofollow,noindex
        response = self.client.get("/judgments/search?query=waltham+forest")
        self.assertContains(response, '<meta name="robots" content="noindex,nofollow" />', html=True)

    @patch("judgments.views.detail.DocumentPdf")
    @patch("judgments.views.detail.requests.get")
    def test_aws_pdf(self, mock_get, mock_pdf):
        url = "https://assets.caselaw.nationalarchives.gov.uk/eat/2023/1/eat_2023_1.pdf"
        mock_pdf.return_value.generate_uri.return_value = url
        mock_get.return_value.content = b"CAT"
        mock_get.return_value.status_code = 200
        response = self.client.get("/eat/2023/1/data.pdf")
        mock_get.assert_called_with(url)
        self.assertContains(response, "CAT")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.detail.DocumentPdf")
    @patch("judgments.views.detail.requests.get")
    def test_aws_pdf_press_summary(self, mock_get, mock_pdf):
        url = "https://assets.caselaw.nationalarchives.gov.uk/eat/2023/1/press-summary/1/eat_2023_1_press-summary_1.pdf"
        mock_pdf.return_value.generate_uri.return_value = url
        mock_get.return_value.content = b"CAT"
        mock_get.return_value.status_code = 200
        response = self.client.get("/eat/2023/1/press-summary/1/data.pdf")
        mock_get.assert_called_with(url)
        self.assertContains(response, "CAT")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.detail.get_document_by_uri")
    def test_xml(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        response = self.client.get("/eat/2023/1/data.xml")
        mock_get_document_by_uri.assert_called_with("eat/2023/1", cache_if_not_found=False)
        self.assertContains(response, "This is a judgment in XML.")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.detail.get_document_by_uri")
    def test_xml_press_summary(self, mock_get_document_by_uri):
        mock_get_document_by_uri.return_value = JudgmentFactory.build(is_published=True)
        response = self.client.get("/eat/2023/1/press-summary/1/data.xml")
        mock_get_document_by_uri.assert_called_with("eat/2023/1/press-summary/1", cache_if_not_found=False)
        self.assertContains(response, "This is a judgment in XML.")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch.object(PdfDetailView, "pdf_stylesheets", [])
    @patch("judgments.views.detail.PdfDetailView.get_context_data")
    def test_weasy_pdf(self, mock_context):
        mock_context.return_value = {"judgment": "<cat>KITTEN</cat>"}
        response = self.client.get("/eat/2023/1/generated.pdf")
        mock_context.assert_called_with(document_uri="eat/2023/1")
        self.assertContains(response, b"%PDF-1.7")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch.object(PdfDetailView, "pdf_stylesheets", [])
    @patch("judgments.views.detail.PdfDetailView.get_context_data")
    def test_weasy_pdf_press_summary(self, mock_context):
        mock_context.return_value = {"judgment": "<cat>KITTEN</cat>"}
        response = self.client.get("/eat/2023/1/press-summary/1/generated.pdf")
        mock_context.assert_called_with(document_uri="eat/2023/1/press-summary/1")
        self.assertContains(response, b"%PDF-1.7")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.feeds.search_judgments_and_parse_response")
    def test_static_page(self, mock_search_judgments_and_parse_response):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        # The judgment search results page should have a robots meta tag
        # with nofollow,noindex
        response = self.client.get("/about-this-service")
        assert "noindex" not in response.content.decode("utf-8")
        assert "Find Case Law is a service that provides public access to court judgments" in response.content.decode(
            "utf-8",
        )

    def test_static_pages(self):
        for url in [
            "computational-licence-form",
            "transactional-licence-form",
            "what-to-expect",
            "about-this-service",
            "how-to-use-this-service",
            "privacy-notice",
            "accessibility-statement",
            "open-justice-licence",
            "terms-of-use",
            "publishing-policy",
            "robots.txt",
        ]:
            response = self.client.get(f"/{url}", follow=True)
            assert response.status_code == 200


class TestBackLink(TestCase):
    def test_referrer_is_search_page_without_query(self):
        assert search_context_from_url("https://example.com/judgments/search") == {
            "search_url": "https://example.com/judgments/search",
            "query": None,
        }

    def test_referrer_is_search_page_with_query(self):
        # When there is a referrer, and it is a results page,
        # the back link is displayed:
        assert search_context_from_url("https://example.com/judgments/search?query=test+query") == {
            "search_url": "https://example.com/judgments/search?query=test+query",
            "query": "test query",
        }

    def test_referrer_not_results_or_advanced_search_page(self):
        self.assertIs(search_context_from_url("https://example.com/any/other/path"), None)

    def test_no_referrer(self):
        self.assertIs(search_context_from_url(None), None)


def test_min_max():
    assert clamp(0, minimum=1) == 1
    assert clamp(0, minimum=1) == 1
    assert clamp(2, 1, 3) == 2
    assert clamp(2, 1) == 2
    assert clamp(5, 1, 3) == 3
    assert clamp(2, minimum=1, maximum=3) == 2


def test_preprocess_query():
    # Stopwords are removed
    assert utils.preprocess_query("weight of evidence") == "weight evidence"
    # Quotes are normalised
    assert utils.preprocess_query("“excessively difficult”") == '"excessively difficult"'
    # Quote normalisation happens before stopwords are removed, so curly quoted # strings retain stopwords:
    assert utils.preprocess_query("“weight of evidence”") == '"weight of evidence"'
    # "vs", "- v -", etc are stopwords,
    assert utils.preprocess_query("Riley vs Murray") == "Riley Murray"
    assert utils.preprocess_query("Riley - v - Murray") == "Riley Murray"
    assert utils.preprocess_query("Riley -v- Murray") == "Riley Murray"

    # multiple spaces are normalised:

    assert utils.preprocess_query("Riley       v       Murray") == "Riley Murray"
    assert utils.preprocess_query("Riley  -    vs  -   Murray") == "Riley Murray"

    # a separator is required around v

    assert utils.preprocess_query("environment") == "environment"


def test_normalise_quotes():
    # Curly double quotes are replaced by straight ones
    assert utils.normalise_quotes("“excessively difficult”") == '"excessively difficult"'


def test_remove_unquoted_stop_words():
    # Stopwords outside quoted strings are removed.
    assert utils.remove_unquoted_stop_words("weight of evidence") == "weight evidence"
    # Stopwords inside quoted strings are removed
    assert utils.remove_unquoted_stop_words('"weight of evidence"') == '"weight of evidence"'

    assert utils.remove_unquoted_stop_words("the") == "the"
    assert utils.remove_unquoted_stop_words('"the"') == '"the"'
    assert utils.remove_unquoted_stop_words("judge and jury") == "judge jury"
    assert utils.remove_unquoted_stop_words('"judge and jury"') == '"judge and jury"'


def test_without_stop_word_regex():
    stop_words = ["and", "of", "the", "for"]
    expected_output = r"(\band\b)|(\bof\b)|(\bthe\b)|(\bfor\b)"
    assert utils.without_stop_words_regex(stop_words) == expected_output


def test_solo_stop_word_regex():
    stop_words = ["and", "of", "the", "for"]
    expected_output = r"(^and$)|(^of$)|(^the$)|(^for$)"
    assert utils.solo_stop_word_regex(stop_words) == expected_output
