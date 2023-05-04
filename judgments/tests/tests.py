import re
from os import environ
from unittest import skip
from unittest.mock import patch

import pytest
from django.test import TestCase
from factories import JudgmentFactory
from test_search import fake_search_result, fake_search_results

from judgments import converters, utils
from judgments.models import CourtDates
from judgments.utils import as_integer, display_back_link, paginator
from judgments.views.detail import get_pdf_size


class TestJudgment(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_published_judgment_response(self, mock_judgment, mock_pdf_size):
        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = "1234KB"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

        self.assertIn("<p>This is a judgment in HTML.</p>", decoded_response)
        self.assertIn(
            '<meta name="robots" content="noindex,nofollow" />', decoded_response
        )

        self.assertEqual(response.status_code, 200)

    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_judgment_not_published_404_response(self, mock_judgment):
        mock_judgment.return_value = JudgmentFactory.build(is_published=False)

        response = self.client.get("/test/2023/123")

        decoded_response = response.content.decode("utf-8")
        self.assertIn("Page not found", decoded_response)
        self.assertEqual(response.status_code, 404)

    @patch(
        "caselawclient.models.judgments.Judgment.judgment_exists",
        return_value=False,
    )
    def test_judgment_not_found_404_response(self, exists):
        response = self.client.get("/test/2023/123")

        decoded_response = response.content.decode("utf-8")
        self.assertIn("Page not found", decoded_response)
        self.assertEqual(response.status_code, 404)


class TestCourtDates(TestCase):
    def setUp(self):
        CourtDates.objects.create(
            param="earliest_starting_court", start_year=2001, end_year=2020
        )
        CourtDates.objects.create(
            param="last_ending_court", start_year=2005, end_year=2023
        )

    def test_min_year(self):
        self.assertEqual(CourtDates.min_year(), 2001)

    def test_max_year(self):
        self.assertEqual(CourtDates.max_year(), 2023)


class TestJudgmentPdfLinkText(TestCase):
    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_judgment_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_size(self, mock_judgment, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns a non-empty string (either a file size or
        "unknown"), in which case we should link to the file in S3 via our assets URL and display the size string.
        """

        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = " (1234KB)"

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertIn(
            "https://example.com/test/2023/123/test_2023_123.pdf", decoded_response
        )
        self.assertNotIn("data.pdf", decoded_response)
        self.assertIn("(1234KB)", decoded_response)

    @patch("judgments.views.detail.get_pdf_size")
    @patch("judgments.views.detail.get_judgment_by_uri")
    @patch.dict(environ, {"ASSETS_CDN_BASE_URL": "https://example.com"})
    def test_pdf_link_with_no_size(self, mock_judgment, mock_pdf_size):
        """
        `get_pdf_size` serves several purposes; it can _either_ return a string with the size of a PDF if one exists
        in S3, _or_ return a string saying "unknown size" if the file exists but S3 doesn't tell us the size, _or_
        return an empty string. This tests the case where it returns an empty string (implying that the file doesn't
        exist in S3), so we should link to our generated PDF instead and not S3."""

        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        mock_pdf_size.return_value = ""

        response = self.client.get("/test/2023/123")
        decoded_response = response.content.decode("utf-8")

        self.assertNotIn("test_2023_123.pdf", decoded_response)
        self.assertIn("/test/2023/123/data.pdf", decoded_response)


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
        self.assertEqual(paginator(10, 2500), expected_result)

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
        self.assertEqual(paginator(1, 25), expected_result)

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
        self.assertEqual(paginator(1, 5), expected_result)

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
    @patch("judgments.views.index.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_homepage(self, fake_result, fake_advanced_search):
        # The homepage should not have a robots meta tag with nofollow,noindex
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        response = self.client.get("/")
        self.assertNotContains(
            response, '<meta name="robots" content="noindex,nofollow" />'
        )
        self.assertNotEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.results.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_judgment_search_results(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        # The judgment search results page should have a robots meta tag
        # with nofollow,noindex
        response = self.client.get("/judgments/results?query=waltham+forest")
        self.assertContains(
            response, '<meta name="robots" content="noindex,nofollow" />'
        )

    @patch("judgments.views.detail.requests.get")
    def test_aws_pdf(self, get_pdf):
        get_pdf.return_value.content = b"CAT"
        get_pdf.return_value.status_code = 200
        response = self.client.get("/eat/2023/1/data.pdf")
        self.assertContains(response, "CAT")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.detail.get_judgment_by_uri")
    def test_xml(self, mock_judgment):
        mock_judgment.return_value = JudgmentFactory.build(is_published=True)
        response = self.client.get("/eat/2023/1/data.xml")
        self.assertContains(response, "This is a judgment in XML.")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @pytest.mark.local("Needs static file in CI")
    @patch("judgments.views.detail.PdfDetailView.get_context_data")
    def test_weasy_pdf(self, mock_context):
        mock_context.return_value = {"judgment": "<cat>KITTEN</cat>"}
        response = self.client.get("/eat/2023/1/generated.pdf")
        self.assertContains(response, b"%PDF-1.7")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex,nofollow")

    @patch("judgments.views.results.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_static_page(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        # The judgment search results page should have a robots meta tag
        # with nofollow,noindex
        response = self.client.get("/what-to-expect")
        self.assertNotContains(response, "noindex")
        self.assertContains(response, "Public Records Office")  # actual content of page


class TestBackLink(TestCase):
    def test_referrer_is_results_page(self):
        # When there is a referrer, and it is a results page,
        # the back link is displayed:
        self.assertIs(display_back_link("https://example.com/judgments/results"), True)

    def test_referrer_is_advanced_search_page(self):
        # When there is a referrer and it is the advanced search page,
        # the back link is displayed:
        self.assertIs(
            display_back_link("https://example.com/judgments/advanced_search"), True
        )

    def test_refererrer_not_results_or_advanced_search_page(self):
        # When there is a referrer, but it is not a results page
        # or the advanced search page, the back link is not displayed:
        self.assertIs(display_back_link("https://example.com/any/other/path"), False)

    def test_no_referrer(self):
        # When there is no referrer, the back link is not displayed:
        self.assertIs(display_back_link(None), False)


class TestGetPdfSize(TestCase):
    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_returns_valid_size(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {"Content-Length": "1234567890"}
        mock_head.return_value.status_code = 200
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == " (1.1\xa0GB)"
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )

    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_pdf_exists_with_no_size(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {}
        mock_head.return_value.status_code = 200
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == " (unknown size)"
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )

    @patch("judgments.views.detail.get_pdf_uri")
    @patch("judgments.views.detail.requests.head")
    def test_no_pdf_exists(self, mock_head, mock_get_pdf_uri):
        mock_head.return_value.headers = {}
        mock_head.return_value.status_code = 404
        mock_get_pdf_uri.return_value = "http://example.com/test.pdf"

        assert get_pdf_size("") == ""
        mock_head.assert_called_with(
            "http://example.com/test.pdf", headers={"Accept-Encoding": None}
        )


def test_min_max():
    assert as_integer("cow", minimum=4) == 4
    assert as_integer(0, minimum=1) == 1
    assert as_integer(0, minimum=1) == 1
    assert as_integer(0, minimum=0, default=1) == 0
    assert as_integer(-1, minimum=0, default=1) == 0
    assert as_integer(0, minimum=1, default=10) == 1
    assert as_integer(2, 1, 3) == 2
    assert as_integer(2, 1) == 2
    assert as_integer(5, 1, 3) == 3
    assert as_integer(2, minimum=1, maximum=3) == 2
    assert as_integer(None, minimum=1, default=4) == 4
    assert as_integer(None, minimum=1) == 1


def test_preprocess_query():
    # Stopwords are removed
    assert utils.preprocess_query("weight of evidence") == "weight evidence"
    # Quotes are normalised
    assert (
        utils.preprocess_query("“excessively difficult”") == '"excessively difficult"'
    )
    # Quote normalisation happens before stopwords are removed, so curly quoted # strings retain stopwords:
    assert utils.preprocess_query("“weight of evidence”") == '"weight of evidence"'


def test_normalise_quotes():
    # Curly double quotes are replaced by straight ones
    assert (
        utils.normalise_quotes("“excessively difficult”") == '"excessively difficult"'
    )


def test_remove_unquoted_stop_words():
    # Stopwords outside quoted strings are removed.
    assert utils.remove_unquoted_stop_words("weight of evidence") == "weight evidence"
    # Stopwords inside quoted strings are removed
    assert (
        utils.remove_unquoted_stop_words('"weight of evidence"')
        == '"weight of evidence"'
    )

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
