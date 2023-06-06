from unittest.mock import Mock

from django.test import TestCase

from judgments.templatetags.search_results_filters import is_exact_match


def buildResult(name="Alice Xenakis v Bob Young", ncn="[2023] EWHC 1234 (Ch)"):
    mock = Mock()
    mock.configure_mock(name=name, neutral_citation=ncn)
    return mock


class TestExactMatch(TestCase):
    def test_when_the_name_matches_the_query_exactly(self):
        result = buildResult()
        query = "Alice Xenakis v Bob Young"
        self.assertTrue(is_exact_match(result, query))

    def test_when_the_name_matches_the_query_but_without_a_stopword(self):
        result = buildResult()
        query = "Alice Xenakis Bob Young"
        self.assertTrue(is_exact_match(result, query))

    def test_when_the_name_matches_the_query_but_differs_in_case(self):
        result = buildResult()
        query = "alice xenakis v bob young"
        self.assertTrue(is_exact_match(result, query))

    def test_when_the_name_matches_the_ncn_exactly(self):
        result = buildResult()
        query = "[2023] EWHC 1234 (Ch)"
        self.assertTrue(is_exact_match(result, query))

    def test_when_the_name_matches_the_ncn_but_differs_in_case(self):
        result = buildResult()
        query = "[2023] ewhc 1234 (Ch)"
        self.assertTrue(is_exact_match(result, query))

    def test_when_the_name_matches_the_ncn_but_differs_in_punctuation(self):
        result = buildResult()
        query = "2023 EWHC 1234 Ch"
        self.assertTrue(is_exact_match(result, query))

    def test_when_nothing_matches_the_query(self):
        result = buildResult()
        query = "Carlos Zamora v Bob Young"
        self.assertFalse(is_exact_match(result, query))
