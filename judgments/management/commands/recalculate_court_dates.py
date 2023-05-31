import datetime

from django.core.management.base import BaseCommand
from ds_caselaw_utils import courts

from judgments.models import CourtDates, SearchResult
from judgments.utils import perform_advanced_search


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
        CourtDates.objects.all().delete()
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
        start_year = self._get_year_of_first_document_in_order(
            court.canonical_param, "date", "oldest", court.start_year
        )

        if start_year < 2000:
            self.stdout.write(
                self.style.WARNING(
                    f"Calculated start year of {start_year} seems improbable, \
falling back to config value of {court.start_year}"
                )
            )
            start_year = court.start_year

        return start_year

    def get_end_year(self, court):
        end_year = self._get_year_of_first_document_in_order(
            court.canonical_param, "-date", "newest", court.end_year
        )

        if end_year > datetime.date.today().year:
            self.stdout.write(
                self.style.WARNING(
                    f"Calculated end year of {end_year} is impossible, \
falling back to config value of {court.end_year}"
                )
            )
            end_year = court.end_year

        return end_year

    def _get_year_of_first_document_in_order(
        self, canonical_param, order, document_reference, fallback
    ):
        search_results = perform_advanced_search(
            court=canonical_param,
            order=order,
            per_page=1,
        )

        first_document = SearchResult.create_from_node(search_results.results[0])

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
