from enum import Enum
from typing import Any

from ds_caselaw_utils.courts import Court, CourtWithJurisdiction


class GtmPageType(str, Enum):
    """Canonical GA4/GTM page_type values. Treat as an analytics contract — do not invent ad-hoc strings."""

    INDEX = "index"
    BROWSE = "browse"
    COURT = "court"
    SEARCH_RESULTS = "search results"
    DOCUMENT = "document"
    LICENSE_APPLICATION = "license_application"
    STATIC = "static"


def court_analytics(court: Court) -> dict[str, str]:
    """Return court_code and court_type for a utils Court (or CourtWithJurisdiction)."""
    if isinstance(court, CourtWithJurisdiction):
        return {
            "court_code": str(court.code),
            "court_type": court.court.type.value,
        }
    return {
        "court_code": str(court.code),
        "court_type": court.type.value,
    }


def build_gtm_data_layer(
    *,
    page_type: GtmPageType,
    court: Court | None = None,
    document_noun: str | None = None,
) -> dict[str, Any]:
    """
    Build a dataLayer object for GTM / GA4 custom dimensions.

    Only include keys that have values so GA reports show (not set) rather than empty strings.
    Callers must resolve any Court themselves — this helper does not look courts up.
    """
    payload: dict[str, Any] = {"page_type": page_type.value}
    if court is not None:
        payload.update(court_analytics(court))
    if document_noun:
        payload["document_noun"] = document_noun
    return payload
