from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import Court

SEARCH_SCOPE_LABELS = {
    "higher_courts": "Higher courts and tribunals",
    "other_courts": "Other courts and tribunals",
    "all_courts": "All courts and tribunals",
}

SEARCH_SCOPE_PREFERENCE_COOKIE = "search_scope_preference"
SEARCH_SCOPE_PREFERENCE_COOKIE_MAX_AGE = 365 * 24 * 60 * 60
HOMEPAGE_SCOPES = ("all_courts", "higher_courts")


def get_higher_court_params() -> list[str]:
    return [str(court.canonical_param) for court in get_higher_courts()]


def get_other_courts() -> list[Court]:
    return [court for court in all_courts.get_show_in_search_filters() if not court.is_court_of_record]


def get_higher_courts() -> list[Court]:
    return [
        court for court in all_courts.get_show_in_search_filters() if court.canonical_param and court.is_court_of_record
    ]
