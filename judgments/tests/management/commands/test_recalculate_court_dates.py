import datetime
from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase
from ds_caselaw_utils.courts import CourtParam

from judgments.management.commands.recalculate_court_dates import Command


class TestRecalculateCourtDates(TestCase):
    @patch("judgments.management.commands.recalculate_court_dates.courts.get_all")
    def test_handle_skips_courts_with_no_canonical_param(self, mock_get_all):
        fake_court = MagicMock()
        fake_court.name = "Fake Court"
        fake_court.canonical_param = None
        mock_get_all.return_value = [fake_court]

        out = StringIO()
        call_command("recalculate_court_dates", stdout=out)
        output = out.getvalue()

        self.assertIn("Fake Court has no canonical_param! Skipping.", output)

    @patch("judgments.management.commands.recalculate_court_dates.courts.get_all")
    @patch("judgments.management.commands.recalculate_court_dates.Command.get_start_year")
    @patch("judgments.management.commands.recalculate_court_dates.Command.get_end_year")
    @patch("judgments.management.commands.recalculate_court_dates.CourtDates.objects.update_or_create")
    def test_handle_writes_to_db_if_write_option_given(
        self, mock_update_or_create, mock_get_end_year, mock_get_start_year, mock_get_all
    ):
        court = MagicMock()
        court.name = "Valid Court"
        court.canonical_param = "valid-court"
        mock_get_all.return_value = [court]

        mock_get_start_year.return_value = 2001
        mock_get_end_year.return_value = 2023

        call_command("recalculate_court_dates", "--write")

        mock_update_or_create.assert_called_once_with(
            param="valid-court",
            defaults={"start_year": 2001, "end_year": 2023},
        )

    @patch("judgments.management.commands.recalculate_court_dates.search_judgments_and_parse_response")
    def test_get_year_of_first_document_in_order_returns_correct_year(self, mock_search):
        command = Command()
        court_param = CourtParam("test-court")

        mock_doc = MagicMock()
        mock_doc.date = datetime.date(2020, 5, 17)
        mock_doc.uri = "/judgment/123"
        mock_search.return_value.results = [mock_doc]

        year = command._get_year_of_first_document_in_order(court_param, "date", "oldest", 1990)
        self.assertEqual(year, 2020)

    @patch("judgments.management.commands.recalculate_court_dates.search_judgments_and_parse_response")
    def test_get_year_of_first_document_in_order_falls_back_on_no_results(self, mock_search):
        command = Command()
        court_param = CourtParam("test-court")
        mock_search.return_value.results = []

        year = command._get_year_of_first_document_in_order(court_param, "date", "oldest", 1999)
        self.assertEqual(year, 1999)

    @patch("judgments.management.commands.recalculate_court_dates.search_judgments_and_parse_response")
    def test_get_start_year_falls_back_if_before_2000(self, mock_search):
        command = Command()

        court = MagicMock()
        court.canonical_param = "test-court"
        court.start_year = 2005

        mock_doc = MagicMock()
        mock_doc.date = datetime.date(1995, 1, 1)
        mock_doc.uri = "/judgment/old"
        mock_search.return_value.results = [mock_doc]

        year = command.get_start_year(court)
        self.assertEqual(year, 2005)

    @patch("judgments.management.commands.recalculate_court_dates.search_judgments_and_parse_response")
    def test_get_end_year_falls_back_if_in_future(self, mock_search):
        command = Command()

        court = MagicMock()
        court.canonical_param = "test-court"
        court.end_year = 2022

        future_year = datetime.date.today().year + 1
        mock_doc = MagicMock()
        mock_doc.date = datetime.date(future_year, 1, 1)
        mock_doc.uri = "/judgment/future"
        mock_search.return_value.results = [mock_doc]

        year = command.get_end_year(court)
        self.assertEqual(year, 2022)
