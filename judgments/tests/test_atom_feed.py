from unittest.mock import patch

import defusedxml.ElementTree as ET
from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixture_data import FakeSearchResponse, FakeSearchResponseManyPages


class TestAtomFeed(TestCase):
    namespaces = {
        "": "http://www.w3.org/2005/Atom",
        "tna": "https://caselaw.nationalarchives.gov.uk",
    }

    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_feed_exists(self, mock_api_client, mock_search_judgments_and_parse_response):
        """Check that the feed actually returns something."""
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/atom.xml")

        # that there is a successful response
        self.assertEqual(response.status_code, 200)

        # that it has the expected Content-Type
        self.assertEqual(response["Content-Type"], "application/xml; charset=utf-8")

    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_feed_query_handling(self, mock_api_client, mock_search_judgments_and_parse_response):
        """Check that the feed is performing the expected searches behind the scenes."""
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        self.client.get("/atom.xml")

        # that search_judgments_and_parse_response is called with the expected parameters
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="",
                court="",
                judge=None,
                party=None,
                date_from="1085-01-01",
                date_to=None,
                order="-date",
                page=1,
                page_size=50,
                only_with_html_representation=True,
            ),
        )

    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_feed_metadata(self, mock_api_client, mock_search_judgments_and_parse_response):
        """Check that the basic feed metadata is intact."""
        search_response = FakeSearchResponse()
        mock_search_judgments_and_parse_response.return_value = search_response

        response = self.client.get("/atom.xml")

        feed_xml_tree = ET.fromstring(response.content.decode("utf-8"))

        # We implicitly test that this is an Atom feed in the process of these assertions, since otherwise it won't parse and resolve the namespace.
        feed_id = feed_xml_tree.find("id", self.namespaces)
        assert feed_id is not None
        assert feed_id.text == "https://caselaw.nationalarchives.gov.uk/atom.xml"

        feed_author_name = feed_xml_tree.find("author/name", self.namespaces)
        assert feed_author_name is not None
        assert feed_author_name.text == "The National Archives"

        feed_rights = feed_xml_tree.find("rights", self.namespaces)
        assert feed_rights is not None
        assert feed_rights.text == "https://caselaw.nationalarchives.gov.uk/open-justice-licence"

    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_feed_entry(self, mock_api_client, mock_search_judgments_and_parse_response):
        """Check that a feed has the expected entry format."""
        search_response = FakeSearchResponse()
        mock_search_judgments_and_parse_response.return_value = search_response

        response = self.client.get("/atom.xml")
        feed_xml_tree = ET.fromstring(response.content.decode("utf-8"))

        entry = feed_xml_tree.find("entry", self.namespaces)
        assert entry is not None

        entry_title = entry.find("title", self.namespaces)
        assert entry_title is not None
        assert entry_title.text == "Judgment v Judgement"

        entry_id = entry.find("id", self.namespaces)
        assert entry_id is not None
        assert entry_id.text == "https://caselaw.nationalarchives.gov.uk/id/d-a1b2c3"

        entry_published = entry.find("published", self.namespaces)
        assert entry_published is not None
        assert entry_published.text == "2023-02-03T00:00:00+00:00"

        entry_updated = entry.find("updated", self.namespaces)
        assert entry_updated is not None
        assert entry_updated.text == "2023-02-03T12:34:00+00:00"

        entry_author_name = entry.find("author/name", self.namespaces)
        assert entry_author_name is not None
        assert entry_author_name.text == "Court of Testing"

        entry_tna_contenthash = entry.find("tna:contenthash", self.namespaces)
        assert entry_tna_contenthash is not None
        assert entry_tna_contenthash.text == "ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73"

        entry_tna_neutral_citation = entry.find("tna:identifier", self.namespaces)
        assert entry_tna_neutral_citation is not None
        assert entry_tna_neutral_citation.text == "[2025] UKSC 123"
        assert entry_tna_neutral_citation.attrib["type"] == "ukncn"
        assert entry_tna_neutral_citation.attrib["slug"] == "uksc/2025/123"

        entry_tna_uri = entry.find("tna:uri", self.namespaces)
        assert entry_tna_uri is not None
        assert entry_tna_uri.text == "d-a1b2c3"

        assets_tna_uri = entry.find("tna:assets_base", self.namespaces)
        assert assets_tna_uri is not None
        assert assets_tna_uri.attrib["href"] == "https://assets.caselaw.nationalarchives.gov.uk/d-a1b2c3/"

        self.assertCountEqual(
            [e.attrib for e in entry.findall("link", self.namespaces)],
            [
                {
                    "href": "http://testserver/uksc/2025/1",
                    "rel": "alternate",
                },
                {
                    "href": "http://testserver/uksc/2025/1/data.xml",
                    "rel": "alternate",
                    "type": "application/akn+xml",
                },
                {
                    "href": "https://assets.caselaw.nationalarchives.gov.uk/d-a1b2c3/d-a1b2c3.pdf",
                    "rel": "alternate",
                    "type": "application/pdf",
                },
            ],
        )

    @patch("judgments.feeds.search_judgments_and_parse_response")
    @patch("judgments.feeds.api_client")
    def test_search_query_in_URL(self, mock_api_client, mock_search):
        search_response = FakeSearchResponseManyPages()
        mock_search.return_value = search_response

        response = self.client.get("/atom.xml?query=obscure-search-query&page=5&order=date")
        decoded_response = response.content.decode("utf-8")

        # that search_judgments_and_parse_response is called with the appropriate parameters
        mock_search.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="obscure-search-query",
                court="",
                judge=None,
                party=None,
                date_from="1085-01-01",
                date_to=None,
                order="date",
                page=5,
                only_with_html_representation=True,
            ),
        )

        self.assertIn('Latest documents for "obscure-search-query"', decoded_response)

        self.assertIn(
            '"https://caselaw.nationalarchives.gov.uk/atom.xml?query=obscure-search-query&amp;order=date"',
            decoded_response,
        )
        self.assertIn(
            '"https://caselaw.nationalarchives.gov.uk/atom.xml?query=obscure-search-query&amp;order=date&amp;page=4"',
            decoded_response,
        )
        self.assertIn(
            '"https://caselaw.nationalarchives.gov.uk/atom.xml?query=obscure-search-query&amp;order=date&amp;page=6"',
            decoded_response,
        )
        self.assertIn(
            '"https://caselaw.nationalarchives.gov.uk/atom.xml?query=obscure-search-query&amp;order=date&amp;page=100"',
            decoded_response,
        )

    @patch("judgments.feeds.search_judgments_and_parse_response")
    def test_feed_with_empty_date(self, mock_search):
        mock_search.return_value = FakeSearchResponse()

        response = self.client.get("/atom.xml")
        decoded_response = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Judgment v Judgement</title>", decoded_response)

    def test_redirect_full(self):
        response = self.client.get("/ewhc/ch/2024/atom.xml")
        assert response.url == "/atom.xml?court=ewhc%2Fch&from=2024-01-01&to=2024-12-31"  # type: ignore[attr-defined]

    def test_redirect_full_with_params(self):
        response = self.client.get("/ewhc/ch/2024/atom.xml?page=4&order=modified")
        assert response.url == "/atom.xml?page=4&order=modified&court=ewhc%2Fch&from=2024-01-01&to=2024-12-31"  # type: ignore[attr-defined]

    def test_redirect_short_court(self):
        response = self.client.get("/ewhc/atom.xml")
        assert response.url == "/atom.xml?court=ewhc"  # type: ignore[attr-defined]

    def test_redirect_tribunal(self):
        response = self.client.get("/eat/atom.xml")
        assert response.url == "/atom.xml?tribunal=eat"  # type: ignore[attr-defined]

    def test_redirect_year_only(self):
        response = self.client.get("/2024/atom.xml")
        assert response.url == "/atom.xml?from=2024-01-01&to=2024-12-31"  # type: ignore[attr-defined]

    def test_bad_court(self):
        response = self.client.get("/atom.xml?court=tennis")
        assert response.status_code == 400

    def test_bad_tribunal(self):
        response = self.client.get("/atom.xml?tribunal=tennis")
        assert response.status_code == 400
