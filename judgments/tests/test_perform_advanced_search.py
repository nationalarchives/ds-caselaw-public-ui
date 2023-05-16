from unittest.mock import MagicMock, patch

from lxml import etree

from judgments.models import SearchResults
from judgments.utils import perform_advanced_search


@patch("judgments.utils.api_client.advanced_search")
def test_perform_advanced_search(mock_advanced_search):
    """
    Given the search parameters for perform_advanced_search are valid
    And a mocked api_client response with 2 search results
    When perform_advanced_search function is called with the mocked API client
        and input parameters
    Then the API client's advanced_search method should be called once with the
        appropriate parameters
    Then the perform_advanced_search function should return an instance of
        SearchResults with 2 results
    And the SearchResults object should have 2 SearchResult objects, each with
        the correct
        index, URI, path, score, confidence, fitness, and extracted properties set on it
    And each of their xml should match the xml for each searchresult elements in the
        response object
    """
    # Set up mocked response
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.headers = {"content-type": "multipart/mixed; boundary=foo"}

    response_mock.content = (
        b"\r\n--foo\r\n"
        b'Content-Type: application/xml\r\nX-Primitive: element()\r\nX-Path: /*:response\r\n\r\n<search:response snippet-format="empty-snippet" total="2" start="1" page-length="10" selected="include" xmlns:search="http://marklogic.com/appservices/search">\n '  # noqa: E501
        b'<search:result index="1" uri="/a/b/2011/10.xml" path="fn:doc(&quot;/a/b/2011/10.xml&quot;)" score="40610" confidence="0.8589264" fitness="0.7958274">\n    <search:snippet/>\n    <search:extracted kind="element"><FRBRdate date="2015-09-18" name="hearing" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><FRBRname value="Made up case name" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><FRBRdate date="2023-01-08T15:56:54" name="transform" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">A-B</uk:court><uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">[2011] A 10 (B)</uk:cite><uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">6462e5941da438fb7a6f042d3958a0d8cc3d75ddc7c1d6e27l50gfi2713302e</uk:hash><neutralCitation style="font-family:\'Book Antiqua\';color:#000000" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">[2011] A 00010 (B)</neutralCitation></search:extracted>\n  </search:result>\n  '  # noqa: E501
        b'<search:result index="2" uri="/a/c/2015/20.xml" path="fn:doc(&quot;/a/c/2015/20.xml&quot;)" score="80180" confidence="0.4589224" fitness="0.2938284">\n    <search:snippet/>\n    <search:extracted kind="element"><FRBRdate date="2017-08-08" name="judgment" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><FRBRname value="Another made up case name" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><FRBRdate date="2023-04-09T18:05:45" name="transform" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/><uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">A-C</uk:court><uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">[2015] A 20 (C)</uk:cite><uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">ce5ghij1158513c5z848bf0f3c637d6c184df809695a693189ed0eb64bc135d9</uk:hash><neutralCitation style="font-weight:bold" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">[2015] A 0020 (C)</neutralCitation></search:extracted>\n  </search:result>\n  '  # noqa: E501
        b"<search:metrics>\n    <search:query-resolution-time>PT0.007706S</search:query-resolution-time>\n    <search:snippet-resolution-time>PT0.000054S</search:snippet-resolution-time>\n    <search:extract-resolution-time>PT0.002231S</search:extract-resolution-time>\n    <search:total-time>PT0.010856S</search:total-time>\n  </search:metrics>\n</search:response>"  # noqa: E501
        b"\r\n--foo--\r\n"
    )

    mock_advanced_search.return_value = response_mock

    # Call perform_advanced_search with mocked api_client and inputs
    search_results = perform_advanced_search(
        query="test query",
        court="test court",
        judge="test judge",
        party="test party",
        neutral_citation="test citation",
        specific_keyword="test keyword",
        date_from="2022-01-01",
        date_to="2022-01-31",
        page=1,
        per_page=10,
    )

    mock_advanced_search.assert_called_once_with(
        q="test query",
        court="test court",
        judge="test judge",
        party="test party",
        neutral_citation="test citation",
        specific_keyword="test keyword",
        page=1,
        order=None,
        date_from="2022-01-01",
        date_to="2022-01-31",
        page_size=10,
        collections=["judgment"],
    )

    # Assert that SearchResults object was created successfully
    assert isinstance(search_results, SearchResults)
    assert search_results.total == "2"
    assert len(search_results.results) == 2
    assert search_results.results[0].attrib == {
        "index": "1",
        "uri": "/a/b/2011/10.xml",
        "path": 'fn:doc("/a/b/2011/10.xml")',
        "score": "40610",
        "confidence": "0.8589264",
        "fitness": "0.7958274",
    }
    assert search_results.results[1].attrib == {
        "index": "2",
        "uri": "/a/c/2015/20.xml",
        "path": 'fn:doc("/a/c/2015/20.xml")',
        "score": "80180",
        "confidence": "0.4589224",
        "fitness": "0.2938284",
    }
    assert (
        etree.tostring(search_results.results[0], pretty_print=True)
        == b'<search:result xmlns:search="http://marklogic.com/appservices/search" index="1" uri="/a/b/2011/10.xml" path="fn:doc(&quot;/a/b/2011/10.xml&quot;)" score="40610" confidence="0.8589264" fitness="0.7958274">\n    <search:snippet/>\n    <search:extracted kind="element"><FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2015-09-18" name="hearing"/><FRBRname xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" value="Made up case name"/><FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2023-01-08T15:56:54" name="transform"/><uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">A-B</uk:court><uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">[2011] A 10 (B)</uk:cite><uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">6462e5941da438fb7a6f042d3958a0d8cc3d75ddc7c1d6e27l50gfi2713302e</uk:hash><neutralCitation xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" style="font-family:\'Book Antiqua\';color:#000000">[2011] A 00010 (B)</neutralCitation></search:extracted>\n  </search:result>\n  \n'  # noqa: E501
    )
    assert (
        etree.tostring(search_results.results[1], pretty_print=True)
        == b'<search:result xmlns:search="http://marklogic.com/appservices/search" index="2" uri="/a/c/2015/20.xml" path="fn:doc(&quot;/a/c/2015/20.xml&quot;)" score="80180" confidence="0.4589224" fitness="0.2938284">\n    <search:snippet/>\n    <search:extracted kind="element"><FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2017-08-08" name="judgment"/><FRBRname xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" value="Another made up case name"/><FRBRdate xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" date="2023-04-09T18:05:45" name="transform"/><uk:court xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">A-C</uk:court><uk:cite xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">[2015] A 20 (C)</uk:cite><uk:hash xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">ce5ghij1158513c5z848bf0f3c637d6c184df809695a693189ed0eb64bc135d9</uk:hash><neutralCitation xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" style="font-weight:bold">[2015] A 0020 (C)</neutralCitation></search:extracted>\n  </search:result>\n  \n'  # noqa: E501
    )
