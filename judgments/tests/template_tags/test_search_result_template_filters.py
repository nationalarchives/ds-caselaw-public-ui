from unittest.mock import Mock

from judgments.templatetags.search_results_filters import show_matches


def test_show_matches_returns_true_when_result_has_matches_and_is_not_exact_match():
    result = Mock()
    result.name = "Example judgment"
    result.neutral_citation = "[2025] UKSC 1"
    result.matches = ["Example highlighted match"]

    assert show_matches(result, "different query") is True
