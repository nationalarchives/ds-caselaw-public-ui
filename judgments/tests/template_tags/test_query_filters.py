import unittest

from judgments.templatetags.query_filters import replace_year_in_query


class TestQueryFilters(unittest.TestCase):
    def test_replace_year_in_query(self):
        query_params = {
            "from_date_0": "3",
            "from_date_1": "9",
            "from_date_2": "2009",
            "to_date_0": "7",
            "to_date_1": "10",
            "to_date_2": "2019",
            "per_page": "10",
        }

        replaced = replace_year_in_query(query_params, "2015")

        self.assertNotIn("from_date_0=", replaced)
        self.assertNotIn("from_date_1=", replaced)
        self.assertNotIn("to_date_0=", replaced)
        self.assertNotIn("to_date_1=", replaced)
        self.assertIn("from_date_2=2015", replaced)
        self.assertIn("to_date_2=2015", replaced)
