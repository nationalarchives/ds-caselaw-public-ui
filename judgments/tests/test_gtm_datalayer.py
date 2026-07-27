from ds_caselaw_utils.courts import courts as all_courts
from ds_caselaw_utils.types import CourtCode, CourtParam

from judgments.utils.gtm_datalayer import (
    build_gtm_data_layer,
    court_analytics,
    court_analytics_from_code,
    court_analytics_from_param,
)


class TestBuildGtmDataLayer:
    def test_page_type_only(self):
        assert build_gtm_data_layer(page_type="static") == {"page_type": "static"}

    def test_omits_empty_optional_fields(self):
        assert build_gtm_data_layer(
            page_type="document",
            court_code="",
            court_type=None,
            document_noun="judgment",
        ) == {
            "page_type": "document",
            "document_noun": "judgment",
        }

    def test_includes_all_fields(self):
        assert build_gtm_data_layer(
            page_type="document",
            court_code="EAT",
            court_type="tribunal",
            document_noun="press summary",
        ) == {
            "page_type": "document",
            "court_code": "EAT",
            "court_type": "tribunal",
            "document_noun": "press summary",
        }


class TestCourtAnalytics:
    def test_court_from_param(self):
        assert court_analytics_from_param("ewhc/ch") == {
            "court_code": str(all_courts.get_by_param(CourtParam("ewhc/ch")).code),
            "court_type": "court",
        }

    def test_tribunal_from_param(self):
        assert court_analytics_from_param("eat") == {
            "court_code": "EAT",
            "court_type": "tribunal",
        }

    def test_unknown_param_returns_empty(self):
        assert court_analytics_from_param("not-a-real-court") == {}

    def test_browse_parent_path_falls_back_to_code(self):
        assert court_analytics_from_param("ewhc") == {
            "court_code": "EWHC",
            "court_type": "court",
        }

    def test_court_from_code(self):
        assert court_analytics_from_code(CourtCode("EAT")) == {
            "court_code": "EAT",
            "court_type": "tribunal",
        }

    def test_unknown_code_returns_empty(self):
        assert court_analytics_from_code("NOT-A-COURT") == {}

    def test_empty_code_returns_empty(self):
        assert court_analytics_from_code("") == {}

    def test_court_with_jurisdiction_uses_base_type(self):
        court = all_courts.get_by_code(CourtCode("UKFTT-GRC/Charity"))
        analytics = court_analytics(court)
        assert analytics == {
            "court_code": "UKFTT-GRC/Charity",
            "court_type": "tribunal",
        }
