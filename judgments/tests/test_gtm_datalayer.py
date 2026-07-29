from ds_caselaw_utils.courts import courts as all_courts
from ds_caselaw_utils.types import CourtCode

from judgments.utils.gtm_datalayer import (
    GtmPageType,
    build_gtm_data_layer,
    court_analytics,
)


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
