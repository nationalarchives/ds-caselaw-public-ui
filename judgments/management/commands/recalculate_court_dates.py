import datetime

from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.core.management.base import BaseCommand
from ds_caselaw_utils import courts

from judgments.models import CourtDates
from judgments.utils import api_client


class Command(BaseCommand):
    help = "Recalculates the date ranges for known courts"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--write",
            action="store_true",
            help="Write changes to the database",
        )

    def handle(self, *args, **options):
        for court in courts.get_all():
            self.stdout.write(self.style.NOTICE(f"{court.name}"))

            if not court.canonical_param:
                self.stdout.write(
                    self.style.ERROR(f"{court.name} has no canonical_param! Skipping.")
                )
                continue

            start_year = self.get_start_year(court)
            end_year = self.get_end_year(court)

            if not options["write"]:
                self.stdout.write(self.style.NOTICE("Skipping write…"))
                continue

            CourtDates.objects.update_or_create(
                param=court.canonical_param,
                defaults={"start_year": start_year, "end_year": end_year},
            )

    def get_start_year(self, court):
        fallback_start_year = court.start_year
        start_year = self._get_year_of_first_document_in_order(
            court.canonical_param, "date", "oldest", fallback_start_year
        )

        if start_year < 2000:
            self.stdout.write(
                self.style.WARNING(
                    f"Calculated start year of {start_year} seems improbable, \
falling back to config value of {fallback_start_year}"
                )
            )
            start_year = fallback_start_year

        return start_year

    def get_end_year(self, court):
        fallback_end_year = court.end_year
        end_year = self._get_year_of_first_document_in_order(
            court.canonical_param, "-date", "newest", fallback_end_year
        )

        if end_year > datetime.date.today().year:
            self.stdout.write(
                self.style.WARNING(
                    f"Calculated end year of {end_year} is impossible, \
falling back to config value of {fallback_end_year}"
                )
            )
            end_year = fallback_end_year

        return end_year

    def _get_year_of_first_document_in_order(
        self, canonical_court_param, order, document_reference, fallback
    ):
        search_response = search_judgments_and_parse_response(
            api_client, SearchParameters(court=canonical_court_param, order=order)
        )

        first_document = search_response.results[0]

        if first_document.date:
            year = first_document.date.year
            self.stdout.write(
                self.style.NOTICE(
                    f"{document_reference.capitalize()} document: {first_document.uri} @ {first_document.date.year}"
                )
            )
        else:
            year = fallback
            self.stdout.write(
                self.style.WARNING(
                    f"Couldn't find date of {document_reference} document {first_document.uri}, \
falling back to config value of {fallback}"
                )
            )
        return year
