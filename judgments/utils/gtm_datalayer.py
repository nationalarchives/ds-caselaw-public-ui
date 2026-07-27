from typing import Any, Optional, Union

from ds_caselaw_utils.courts import Court, CourtNotFoundException, CourtWithJurisdiction
from ds_caselaw_utils.courts import courts as all_courts
from ds_caselaw_utils.types import CourtCode, CourtParam


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


def court_analytics_from_param(param: str) -> dict[str, str]:
    """
    Resolve analytics fields from a court URL param or browse path segment.

    Prefer utils param lookup (e.g. ``ewhc/ch``, ``eat``). Fall back to treating
    the value as a court code (e.g. browse parent path ``ewhc`` → ``EWHC``).
    """
    try:
        return court_analytics(all_courts.get_by_param(CourtParam(param)))
    except CourtNotFoundException:
        return court_analytics_from_code(param.upper())


def court_analytics_from_code(code: Union[str, CourtCode]) -> dict[str, str]:
    if not code:
        return {}
    try:
        return court_analytics(all_courts.get_by_code(CourtCode(str(code))))
    except CourtNotFoundException:
        return {}


def build_gtm_data_layer(
    *,
    page_type: str,
    court_code: Optional[str] = None,
    court_type: Optional[str] = None,
    document_noun: Optional[str] = None,
) -> dict[str, Any]:
    """
    Build a dataLayer object for GTM / GA4 custom dimensions.

    Only include keys that have values so GA reports show (not set) rather than empty strings.
    """
    payload: dict[str, Any] = {"page_type": page_type}
    if court_code:
        payload["court_code"] = court_code
    if court_type:
        payload["court_type"] = court_type
    if document_noun:
        payload["document_noun"] = document_noun
    return payload
