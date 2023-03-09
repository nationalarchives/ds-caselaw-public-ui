import re
from unittest import skip
from unittest.mock import Mock, patch

from django.test import TestCase
from lxml import etree

from judgments import converters, utils
from judgments.models import CourtDates, SearchResult, SearchResults
from judgments.templatetags.court_utils import get_court_date_range, get_court_name
from judgments.utils import as_integer, display_back_link, paginator


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


class TestSearchResults(TestCase):
    @patch("judgments.views.results.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_judgment_results_desktop(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        # The judgment search results view takes the query term from the (desktop) query input
        response = self.client.get(
            "/judgments/results?query=waltham+forest&query_mobile="
        )
        self.assertContains(
            response,
            '<span class="results-search-component__removable-options-value-text">waltham forest</span>',
        )

    @patch("judgments.views.results.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_judgment_results_mobile(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        # The judgment search results view takes the query term from the mobile query input
        response = self.client.get(
            "/judgments/results?query=&query_mobile=waltham+forest"
        )
        self.assertContains(
            response,
            '<span class="results-search-component__removable-options-value-text">waltham forest</span>',
        )


class TestAtomFeed(TestCase):
    @patch("judgments.feeds.perform_advanced_search")
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
        # "?page=" 404s, not 500
        fake_advanced_search.return_value = fake_search_results()
        response = self.client.get("/atom.xml?page=")
        self.assertEqual(response.status_code, 404)


class TestJudgment(TestCase):
    @patch("judgments.views.detail.requests.head")
    @patch("judgments.views.detail.decoder.MultipartDecoder")
    @patch("judgments.views.detail.api_client")
    def test_valid_content(self, client, decoder, head):
        head.return_value.headers = {"Content-Length": "1234567890"}
        client.eval_xslt.return_value = "eval_xslt"
        decoder.MultipartDecoder.from_response.return_value.parts[0].text = "part0text"
        client.get_judgment_name.return_value = "judgment metadata"

        response = self.client.get("/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("assets.caselaw.nationalarchives.gov.uk", decoded_response)
        self.assertIn("ewca_civ_2004_632.pdf", decoded_response)
        self.assertNotIn("data.pdf", decoded_response)
        self.assertIn("(1.1\xa0GB)", decoded_response)
        # We don't use the Download as PDF text because there's an issue with localisated strings on CI
        self.assertEqual(response.status_code, 200)

    @patch("judgments.views.detail.requests.head")
    @patch("judgments.views.detail.decoder.MultipartDecoder")
    @patch("judgments.views.detail.api_client")
    def test_no_valid_pdf(self, client, decoder, head):
        head.return_value.headers = {}
        client.eval_xslt.return_value = "eval_xslt"
        decoder.MultipartDecoder.from_response.return_value.parts[0].text = "part0text"
        client.get_judgment_name.return_value = "judgment metadata"

        response = self.client.get("/ewca/civ/2004/632")
        decoded_response = response.content.decode("utf-8")
        self.assertIn("data.pdf", decoded_response)
        self.assertNotIn("2004_632.pdf", decoded_response)
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


class TestSearchResult(TestCase):
    @patch("judgments.models.api_client")
    def test_create_from_node(self, fake_client):
        client_attrs = {
            "get_property.return_value": "something fake",
            "get_last_modified.return_value": "01-01-2022",
        }
        fake_client.configure_mock(**client_attrs)
        search_result_str = """
        <search:result xmlns:search="http://marklogic.com/appservices/search" index="1" uri="/ukut/lc/2022/241.xml">
            <search:snippet/>
            <search:extracted kind="element">
                <FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2022-09-09" name="decision"/>
                <FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2022-10-10" name="transform"/>
                <FRBRname xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                          value="London Borough of Waltham Forest v Nasim Hussain"/>
                <uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">UKUT-LC</uk:court>
                <uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">[2022] UKUT 241 (LC)</uk:cite>
                <uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
                    56c551fef5be37cb1658c895c1d15c913e76b712ba3ccc88d3b6b75ea69d3e8a
                </uk:hash>
                <neutralCitation xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
                    [2022] UKUT 241 (LC)
                </neutralCitation>
            </search:extracted>
        </search:result>
        """
        search_result_xml = etree.fromstring(search_result_str)
        search_result = SearchResult.create_from_node(search_result_xml)
        self.assertEqual(
            "London Borough of Waltham Forest v Nasim Hussain", search_result.name
        )
        self.assertEqual("ukut/lc/2022/241", search_result.uri)
        self.assertEqual("[2022] UKUT 241 (LC)", search_result.neutral_citation)
        self.assertEqual("UKUT-LC", search_result.court)
        self.assertEqual("2022-09-09", search_result.date)
        self.assertEqual("2022-10-10", search_result.transformation_date)

    @patch("judgments.models.api_client")
    def test_create_from_node_with_missing_elements(self, fake_client):
        client_attrs = {
            "get_property.return_value": "something fake",
            "get_last_modified.return_value": "01-01-2022",
        }
        fake_client.configure_mock(**client_attrs)
        search_result_str = """
        <search:result xmlns:search="http://marklogic.com/appservices/search" index="1" uri="/ukut/lc/2022/241.xml">
            <search:snippet/>
            <search:extracted kind="element">
                <FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2022-09-09" name="decision"/>
                <FRBRname xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                          value="London Borough of Waltham Forest v Nasim Hussain"/>
                <uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"></uk:cite>
                <uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"></uk:court>
                <uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"></uk:hash>
                <uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"></uk:court>
            </search:extracted>
        </search:result>
        """
        search_result_xml = etree.fromstring(search_result_str)
        search_result = SearchResult.create_from_node(search_result_xml)
        self.assertEqual(
            "London Borough of Waltham Forest v Nasim Hussain", search_result.name
        )
        self.assertEqual("ukut/lc/2022/241", search_result.uri)
        self.assertEqual(None, search_result.neutral_citation)
        self.assertEqual(None, search_result.court)
        self.assertEqual(None, search_result.content_hash)


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


class TestRobotsDirectives(TestCase):
    @patch("judgments.views.index.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_homepage(self, fake_result, fake_advanced_search):
        # The homepage should not have a robots meta tag with nofollow,noindex
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        response = self.client.get("/")
        self.assertNotContains(
            response, '<meta name="robots" content="noindex,nofollow">'
        )

    @patch("judgments.views.results.perform_advanced_search")
    @patch("judgments.models.SearchResult.create_from_node")
    def test_judgment_results(self, fake_result, fake_advanced_search):
        fake_advanced_search.return_value = fake_search_results()
        fake_result.return_value = fake_search_result()
        # The judgment search results page should have a robots meta tag
        # with nofollow,noindex
        response = self.client.get("/judgments/results?query=waltham+forest")
        self.assertContains(response, '<meta name="robots" content="noindex,nofollow">')


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


def test_prep_query():
    assert utils.remove_unquoted_stop_words("weight of evidence") == "weight evidence"
    assert (
        utils.remove_unquoted_stop_words("'weight of evidence'")
        == "'weight of evidence'"
    )
    assert utils.remove_unquoted_stop_words("the") == "the"
    assert utils.remove_unquoted_stop_words("'the'") == "'the'"
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


def test_get_court_name():
    assert get_court_name("uksc") == "United Kingdom Supreme Court"


def test_get_court_name_non_existent():
    assert get_court_name("ffff") == ""


@patch("judgments.templatetags.court_utils.CourtDates.objects.get")
class TestCourtDatesHelper(TestCase):
    def mock_court_dates(self, start_year, end_year):
        mock = Mock()
        mock.configure_mock(start_year=start_year, end_year=end_year)
        return mock

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_same(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2011)
        self.assertEqual(get_court_date_range(court), "2011")

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_different(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2011 &ndash; 2012")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_same(self, get):
        get.return_value = self.mock_court_dates(2013, 2013)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_different(
        self, get
    ):
        get.return_value = self.mock_court_dates(2013, 2015)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013 &ndash; 2015")
