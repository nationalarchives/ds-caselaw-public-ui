from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from judgments.search_scopes import get_higher_court_params, get_higher_courts, get_other_courts


class TestSearchScopes(TestCase):
    @patch("judgments.search_scopes.all_courts.get_all")
    def test_courts_are_split_by_court_of_record_status(self, mock_get_all):
        higher = SimpleNamespace(canonical_param="uksc", name="Supreme Court", is_court_of_record=True)
        other = SimpleNamespace(canonical_param="ewcc", name="County Court", is_court_of_record=False)
        unsearchable = SimpleNamespace(canonical_param=None, is_court_of_record=True)
        mock_get_all.return_value = [higher, other, unsearchable, higher]

        self.assertEqual(get_higher_courts(), [higher])
        self.assertEqual(get_other_courts(), [other])
        self.assertEqual(get_higher_court_params(), ["uksc"])
