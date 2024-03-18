from unittest.mock import Mock, call, mock_open, patch

from django.test import TestCase

from judgments.models.court_dates import CourtDates
from judgments.templatetags.court_utils import (
    get_court_crest_path,
    get_court_date_range,
    get_court_intro_text,
    get_court_name,
)


def test_get_court_name():
    assert get_court_name("uksc") == "United Kingdom Supreme Court"


def test_get_court_name_non_existent():
    assert get_court_name("ffff") == ""


@patch("judgments.templatetags.court_utils.CourtDates.objects.get")
class TestCourtDatesHelper(TestCase):
    def mock_court_dates(self, start_year, end_year):
        mock = Mock()
        mock.configure_mock(start_year=start_year, end_year=end_year)
        return mock

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_same(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2011)
        self.assertEqual(get_court_date_range(court), "2011")

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_different(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2011&nbsp;to&nbsp;2012")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_same(self, get):
        get.return_value = self.mock_court_dates(2013, 2013)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_different(
        self, get
    ):
        get.return_value = self.mock_court_dates(2013, 2015)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013&nbsp;to&nbsp;2015")


class TestCourtContentHelpers(TestCase):

    def mock_court_param(self, param):
        mock = Mock()
        mock.configure_mock(canonical_param=param)
        return mock

    @patch("judgments.templatetags.court_utils.finders.find")
    @patch(
        "judgments.templatetags.court_utils.open",
        new_callable=mock_open,
        read_data="# Title\nThe Content.",
        create=True,
    )
    def test_get_court_intro_text_when_intro_exists(self, open, find):
        fs_path = "/path/to_markdown/file.md"
        find.return_value = fs_path
        result = get_court_intro_text(self.mock_court_param("ewhc/mercantile"))
        find.assert_called_with("markdown/court_descriptions/ewhc_mercantile.md")
        open.assert_called_with(fs_path)
        self.assertEqual(result, "<h1>Title</h1>\n<p>The Content.</p>\n")

    @patch("judgments.templatetags.court_utils.finders.find")
    @patch(
        "judgments.templatetags.court_utils.open",
        new_callable=mock_open,
        read_data="# Title\nThe Content.",
        create=True,
    )
    def test_get_court_intro_text_when_intro_does_not_exist(self, open, find):
        fs_path = "/path/to_markdown/file.md"
        find.side_effect = [None, fs_path]
        result = get_court_intro_text(self.mock_court_param("ewhc/mercantile"))
        find.assert_has_calls(
            [
                call("markdown/court_descriptions/ewhc_mercantile.md"),
                call("markdown/court_descriptions/default.md"),
            ]
        )
        open.assert_called_with(fs_path)
        self.assertEqual(result, "<h1>Title</h1>\n<p>The Content.</p>\n")

    @patch("judgments.templatetags.court_utils.finders.find")
    @patch("judgments.templatetags.court_utils.static")
    def test_get_court_crest_path_when_crest_exists(self, static, find):
        fs_path = "/path/to/file.svg"
        static_path = "/static/images/court_crests/ewhc_mercantile.svg"
        find.side_effect = [None, None, None, fs_path]
        static.return_value = static_path
        result = get_court_crest_path(self.mock_court_param("ewhc/mercantile"))
        find.assert_has_calls(
            [
                call("images/court_crests/ewhc_mercantile.gif"),
                call("images/court_crests/ewhc_mercantile.png"),
                call("images/court_crests/ewhc_mercantile.jpg"),
                call("images/court_crests/ewhc_mercantile.svg"),
            ]
        )
        static.assert_called_with("images/court_crests/ewhc_mercantile.svg")
        self.assertEqual(result, static_path)

    @patch("judgments.templatetags.court_utils.finders.find")
    def test_get_court_crest_path_when_crest_does_not_exist(self, find):
        find.side_effect = [None, None, None, None]
        result = get_court_crest_path(self.mock_court_param("ewhc/mercantile"))
        find.assert_has_calls(
            [
                call("images/court_crests/ewhc_mercantile.gif"),
                call("images/court_crests/ewhc_mercantile.png"),
                call("images/court_crests/ewhc_mercantile.jpg"),
                call("images/court_crests/ewhc_mercantile.svg"),
            ]
        )
        self.assertEqual(result, None)
