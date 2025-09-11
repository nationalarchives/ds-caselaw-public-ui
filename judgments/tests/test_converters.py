import datetime
import inspect
import re

import ds_caselaw_utils
from django.test import TestCase
from ds_caselaw_utils import factory

from judgments.converters import (
    ComponentConverter,
    CourtConverter,
    DateConverter,
    DocumentUriConverter,
    FileFormatConverter,
    SubdivisionConverter,
    YearConverter,
    converter_regexes,
)


class TestYearConverter(TestCase):
    def setUp(self):
        self.converter = YearConverter()

    def test_regex_matches_four_digits(self):
        self.assertTrue(re.fullmatch(self.converter.regex, "2020"))
        self.assertTrue(re.fullmatch(self.converter.regex, "0000"))
        self.assertTrue(re.fullmatch(self.converter.regex, "9999"))

        self.assertIsNone(re.fullmatch(self.converter.regex, "20"))
        self.assertIsNone(re.fullmatch(self.converter.regex, "abcd"))
        self.assertIsNone(re.fullmatch(self.converter.regex, "12345"))

    def test_to_python_converts_string_to_int(self):
        self.assertEqual(self.converter.to_python("1999"), 1999)
        self.assertEqual(self.converter.to_python("0001"), 1)

    def test_to_url_formats_int_as_four_digits(self):
        self.assertEqual(self.converter.to_url(5), "0005")
        self.assertEqual(self.converter.to_url(2024), "2024")
        self.assertEqual(self.converter.to_url(0), "0000")


class TestDateConverter(TestCase):
    def setUp(self):
        self.converter = DateConverter()

    def test_regex_matches_valid_date(self):
        valid_dates = ["2023-01-01", "0000-12-31", "1999-11-09"]
        for date_str in valid_dates:
            self.assertIsNotNone(re.fullmatch(self.converter.regex, date_str))

    def test_regex_rejects_invalid_date_formats(self):
        invalid_dates = ["2023/01/01", "20230101", "99-01-01", "2023-1-1", "abcd-ef-gh"]
        for date_str in invalid_dates:
            self.assertIsNone(re.fullmatch(self.converter.regex, date_str))

    def test_to_python_converts_string_to_datetime(self):
        result = self.converter.to_python("2024-06-17")
        expected = datetime.datetime(2024, 6, 17)
        self.assertEqual(result, expected)

    def test_to_url_formats_datetime_as_string(self):
        dt = datetime.datetime(2025, 1, 5)
        self.assertEqual(self.converter.to_url(dt), "2025-01-05")

    def test_to_url_raises_value_error_on_none(self):
        with self.assertRaises(ValueError):
            self.converter.to_url(None)


class TestCourtConverter(TestCase):
    def setUp(self):
        self.converter = CourtConverter()

    def test_regex_matches_valid_court_codes(self):
        valid_codes = [
            "ewhc",
            "uksc",
            "ukpc",
            "ewca",
            "ewcop",
            "ewfc",
            "ukut",
            "eat",
            "ukftt",
            "ukait",
            "ukiptrib",
            "ewcc",
            "ewcr",
        ]

        for code in valid_codes:
            self.assertIsNotNone(re.fullmatch(self.converter.regex, code))

    def test_regex_rejects_invalid_court_codes(self):
        invalid_codes = ["EWCA", "ukft", "ew", "ewhc1", "abc", "", "1234", "ukpcx"]

        for code in invalid_codes:
            self.assertIsNone(re.fullmatch(self.converter.regex, code))

    def test_to_python_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_python("ewhc"), "ewhc")

    def test_to_url_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_url("uksc"), "uksc")


class TestSubdivisionConverter(TestCase):
    def setUp(self):
        self.converter = SubdivisionConverter()

    def test_regex_matches_valid_subdivisions(self):
        valid_subdivision_codes = [
            "civ",
            "crim",
            "admin",
            "admlty",
            "ch",
            "comm",
            "costs",
            "fam",
            "ipec",
            "mercantile",
            "pat",
            "qb",
            "kb",
            "iac",
            "lc",
            "tcc",
            "aac",
            "scco",
            "tc",
            "grc",
            "b",
            "t1",
            "t2",
            "t3",
        ]

        for subdivision_code in valid_subdivision_codes:
            self.assertIsNotNone(re.fullmatch(self.converter.regex, subdivision_code))

    def test_regex_rejects_invalid_subdivisions(self):
        invalid_subdivision_codes = ["CIV", "criminal", "civil", "t4", "t", "x1", "", "123", "patent", "qb1"]

        for subdivision_code in invalid_subdivision_codes:
            self.assertIsNone(re.fullmatch(self.converter.regex, subdivision_code))

    def test_to_python_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_python("fam"), "fam")

    def test_to_url_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_url("tcc"), "tcc")


class TestFileFormatConverter(TestCase):
    def setUp(self):
        self.converter = FileFormatConverter()

    def test_regex_matches_valid_file_formats(self):
        valid_file_formats = ["data.pdf", "generated.pdf", "data.xml", "data.html"]

        for file_format in valid_file_formats:
            self.assertIsNotNone(re.fullmatch(self.converter.regex, file_format))

    def test_regex_rejects_invalid_file_formats(self):
        invalid_file_formats = ["data.docx", "judgment.xml", "data.gif"]

        for file_format in invalid_file_formats:
            self.assertIsNone(re.fullmatch(self.converter.regex, file_format))

    def test_to_python_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_python("data.pdf"), "data.pdf")

    def test_to_url_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_url("data.html"), "data.html")


class TestDocumentUriConverter(TestCase):
    def setUp(self):
        self.converter = DocumentUriConverter()

    def test_regex_matches_valid_document_uris(self):
        valid_uris = ["ewca/civ/2025/abc", "ewca/civ/2025/a-b-c", "ewca/civ/2025/a.b.c"]
        for uri in valid_uris:
            self.assertIsNotNone(re.fullmatch(self.converter.regex, uri))

    def test_regex_rejects_invalid_document_uris(self):
        invalid_uris = [
            "UPPERCASETOOLOUD",
            "spaces are bad",
            "spec!al&ch@racters",
            "with-a-hash#",
            "",
        ]
        for uri in invalid_uris:
            self.assertIsNone(re.fullmatch(self.converter.regex, uri))

    def test_to_python_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_python("ewca/civ/2025/abc"), "ewca/civ/2025/abc")

    def test_to_url_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_url("ewca/civ/2025/abc"), "ewca/civ/2025/abc")


class TestComponentConverter(TestCase):
    def setUp(self):
        self.converter = ComponentConverter()

    def test_regex_matches_valid_component(self):
        self.assertIsNotNone(re.fullmatch(self.converter.regex, "press-summary"))

    def test_regex_rejects_invalid_components(self):
        invalid_components = ["press_summary", "presssummary", "summary", "", "PRESS-SUMMARY"]

        for value in invalid_components:
            self.assertIsNone(re.fullmatch(self.converter.regex, value))

    def test_to_python_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_python("press-summary"), "press-summary")

    def test_to_url_returns_value_unchanged(self):
        self.assertEqual(self.converter.to_url("press-summary"), "press-summary")


class TestConverterRegexes:
    def test_converter_regex(self):
        data = [
            {
                "name": "court_group1",
                "is_tribunal": False,
                "courts": [{"param": "court1/jam", "name": "Court 1 Jam"}],
            },
            {
                "name": "court_group2",
                "is_tribunal": False,
                "courts": [{"param": "court2/jam", "name": "Court 2 Jam"}],
            },
            {
                "name": "court_group3",
                "is_tribunal": False,
                "courts": [{"param": "court2/eggs", "name": "Court 2 Eggs", "extra_params": ["court3/bacon"]}],
            },
            {
                "name": "court_group4",
                "is_tribunal": False,
                "courts": [{"name": "Has no params"}],
            },
        ]
        valid_data = factory.make_court_repo_valid(data)
        # this next bit is a mess because ds_caselaw_utils' courts.py is shadowed by the list of courts :(
        module = inspect.getmodule(ds_caselaw_utils.courts)
        assert module
        repo = module.CourtsRepository(valid_data)
        assert converter_regexes(repo) == ("court1|court2|court3", "bacon|eggs|jam")
