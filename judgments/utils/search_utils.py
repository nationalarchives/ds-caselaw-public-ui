from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import CourtNotFoundException


def process_facets(facets: dict):
    """
        Util for processing court facets
    """
    unprocessed_facets = facets.copy()
    court_facets = {}
    for facet_key, facet_value in facets.items():
        try:
            court_code = all_courts.get_by_code(facet_key)
        except CourtNotFoundException:
            continue
        court_facets[court_code] = facet_value
        # Once we have handled a facet, remove it from facets.
        unprocessed_facets.pop(facet_key)
    return unprocessed_facets, court_facets
