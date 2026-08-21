from dataclasses import dataclass
from datetime import date
from typing import Any

from ds_caselaw_utils.courts import courts as all_courts
from ds_caselaw_utils.types import CourtCode

from judgments.utils.gtm_datalayer import (
    GtmPageType,
    build_gtm_data_layer,
    build_search_data_layer,
    court_analytics,
)


@dataclass
class FakeSearchDataForm:
    cleaned_data: dict[str, Any]


class TestBuildGtmDataLayer:
    def test_page_type_only(self):
        assert build_gtm_data_layer(page_type=GtmPageType.STATIC) == {"page_type": "static"}

    def test_omits_empty_optional_fields(self):
        assert build_gtm_data_layer(
            page_type=GtmPageType.DOCUMENT,
            document_noun="judgment",
        ) == {
            "page_type": "document",
            "document_noun": "judgment",
        }

    def test_includes_court_and_document_noun(self):
        court = all_courts.get_by_code(CourtCode("EAT"))
        assert build_gtm_data_layer(
            page_type=GtmPageType.DOCUMENT,
            court=court,
            document_noun="press summary",
        ) == {
            "page_type": "document",
            "court_code": "EAT",
            "court_type": "tribunal",
            "document_noun": "press summary",
        }

    def test_includes_search_data(self):
        assert build_gtm_data_layer(
            page_type=GtmPageType.SEARCH_RESULTS,
            search_data={"search_query": "waltham forest", "search_results_count": 12},
        ) == {
            "page_type": "search results",
            "search_query": "waltham forest",
            "search_results_count": 12,
        }


class TestBuildSearchDataLayer:
    def test_includes_supplied_search_filters_and_result_count(self):
        form = FakeSearchDataForm(
            cleaned_data={
                "query": "waltham forest",
                "court": ["ewhc/ch", "ewhc/ipec"],
                "tribunal": ["eat"],
                "party": "Smith",
                "judge": "Jones",
                "from_date": date(2024, 1, 1),
                "to_date": date(2024, 12, 31),
            }
        )

        assert build_search_data_layer(form, 42) == {
            "search_results_count": 42,
            "search_query": "waltham forest",
            "search_party": "Smith",
            "search_judge": "Jones",
            "search_court": "ewhc/ch,ewhc/ipec",
            "search_tribunal": "eat",
            "search_from_date": "2024-01-01",
            "search_to_date": "2024-12-31",
        }

    def test_omits_empty_filters_but_keeps_zero_result_count(self):
        form = FakeSearchDataForm(cleaned_data={})

        assert build_search_data_layer(form, 0) == {"search_results_count": 0}


class TestCourtAnalytics:
    def test_court(self):
        court = all_courts.get_by_code(CourtCode("EAT"))
        assert court_analytics(court) == {
            "court_code": "EAT",
            "court_type": "tribunal",
        }

    def test_court_with_jurisdiction_uses_base_type(self):
        court = all_courts.get_by_code(CourtCode("UKFTT-GRC/Charity"))
        assert court_analytics(court) == {
            "court_code": "UKFTT-GRC/Charity",
            "court_type": "tribunal",
        }
