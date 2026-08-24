import unittest
from typing import Any

from judgments.templatetags.query_filters import (
    make_query_string,
    removable_filter_param,
    remove_court,
    remove_query,
    replace_integer_with_day,
    replace_integer_with_month,
)


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

    def test_removable_filter_param(self):
        self.assertTrue(removable_filter_param("judge"))

    def test_replace_integer_with_day(self):
        self.assertEqual(replace_integer_with_day(3), "03")

    def test_replace_integer_with_month(self):
        self.assertEqual(replace_integer_with_month(9), "Sep")
