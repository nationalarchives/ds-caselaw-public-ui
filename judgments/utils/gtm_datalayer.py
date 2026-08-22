from enum import Enum
from typing import Any, Protocol

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
    search_data: dict[str, Any] | None = None,
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
    if search_data:
        payload.update(search_data)
    return payload


class SearchDataForm(Protocol):
    cleaned_data: dict[str, Any]


def build_search_data_layer(form: SearchDataForm, results_count: int) -> dict[str, Any]:
    """
    Build analytics metadata for user-entered advanced search filters.
    """
    data_layer: dict[str, Any] = {"search_results_count": results_count}

    for field_name, data_layer_key in [
        ("query", "search_query"),
        ("party", "search_party"),
        ("judge", "search_judge"),
    ]:
        if value := form.cleaned_data.get(field_name):
            data_layer[data_layer_key] = value

    for field_name, data_layer_key in [
        ("court", "search_court"),
        ("tribunal", "search_tribunal"),
    ]:
        values = form.cleaned_data.get(field_name, [])
        if values:
            data_layer[data_layer_key] = ",".join(values)

    for field_name, data_layer_key in [
        ("from_date", "search_from_date"),
        ("to_date", "search_to_date"),
    ]:
        if value := form.cleaned_data.get(field_name):
            data_layer[data_layer_key] = value.isoformat()

    return data_layer
