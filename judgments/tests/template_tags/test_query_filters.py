import unittest
from typing import Any

from judgments.templatetags.query_filters import make_query_string, remove_court, remove_query, replace_year_in_query


class TestQueryFilters(unittest.TestCase):
    def test_remove_query_removes_filter(self):
        query_params: dict[str, Any] = {
            "query": "Imperial",
            "judge": "Someone",
            "page": "3",
            "order": "-date",
        }

        result = remove_query(query_params, "judge")

        self.assertEqual(result, "query=Imperial")

    def test_remove_query_removes_date_filter(
        self,
    ):
        query_params: dict[str, Any] = {
            "query": "Imperial",
            "from_date_0": "3",
            "from_date_1": "9",
            "from_date_2": "2009",
            "page": "3",
            "order": "-date",
        }

        result = remove_query(query_params, "from")

        self.assertEqual(result, "query=Imperial")

    def test_remove_court(self):
        query_params: dict[str, Any] = {
            "query": "Imperial",
            "court": ["ewhc/ipec", "ewhc/ch"],
            "tribunal": ["ukiptrib"],
            "page": "3",
            "order": "-date",
        }

        result = remove_court(query_params, "ewhc/ipec")

        self.assertIn("query=Imperial", result)
        self.assertIn("court=ewhc/ch", result)
        self.assertNotIn("court=ewhc/ipec", result)
        self.assertIn("tribunal=ukiptrib", result)
        self.assertNotIn("page=", result)
        self.assertNotIn("order=", result)

    def test_remove_court_from_both_court_and_tribunal(self):
        query_params: dict[str, Any] = {
            "court": ["ewhc/ipec", "ewhc/ch"],
            "tribunal": ["ewhc/ipec", "ukiptrib"],
        }

        result = remove_court(query_params, "ewhc/ipec")

        self.assertNotIn("ewhc/ipec", result)
        self.assertIn("court=ewhc/ch", result)
        self.assertIn("tribunal=ukiptrib", result)

    def test_make_query_string(self):
        query_params = {
            "query": "Imperial",
            "page": "2",
            "from_date_0": "",
            "to_date_0": None,
        }

        query_string = make_query_string(query_params)

        self.assertIn("query=Imperial", query_string)
        self.assertIn("page=2", query_string)
        self.assertNotIn("from_date_0=", query_string)
        self.assertNotIn("to_date_0=", query_string)

    def test_make_query_string_returns_empty_string_for_falsy_values(self):
        query_params: dict[str, Any] = {
            "empty": "",
            "none": None,
            "zero": 0,
            "false": False,
            "items": [],
        }

        query_string = make_query_string(query_params)

        self.assertEqual(query_string, "")

    def test_replace_year_in_query(self):
        query_params: dict[str, Any] = {
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
