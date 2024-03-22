import unittest

from judgments.templatetags.query_filters import replace_year_in_query


class TestQueryFilters(unittest.TestCase):
    def test_replace_year_in_query(self):
        query_params = {
            "from": "2010",
            "from_day": "3",
            "from_month": "9",
            "from_year": "2009",
            "to": "2014",
            "to_day": "7",
            "to_month": "10",
            "to_year": "2019",
            "per_page": "10",
        }

        replaced = replace_year_in_query(query_params, "2015")

        self.assertNotIn("from_day=", replaced)
        self.assertNotIn("from_month=", replaced)
        self.assertNotIn("to_day=", replaced)
        self.assertNotIn("to_month=", replaced)
        self.assertNotIn("to=", replaced)
        self.assertNotIn("from=", replaced)
        self.assertIn("from_year=2015", replaced)
        self.assertIn("to_year=2015", replaced)
