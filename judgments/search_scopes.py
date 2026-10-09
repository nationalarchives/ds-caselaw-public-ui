from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import Court

SEARCH_SCOPE_LABELS = {"higher_courts": "Higher courts"}

def _get_courts_by_param() -> list[Court]:
    # Historical court codes can share a search parameter; render it only once.
    return list({court.canonical_param: court for court in all_courts.get_all() if court.canonical_param}.values())


def get_higher_court_params() -> list[str]:
    return [str(court.canonical_param) for court in get_higher_courts()]


def get_other_courts() -> list[Court]:
    return [court for court in _get_courts_by_param() if not court.is_court_of_record]


def get_higher_courts() -> list[Court]:
    return [court for court in _get_courts_by_param() if court.is_court_of_record]
