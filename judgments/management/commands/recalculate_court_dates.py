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
            if court.canonical_param:
                search_results = perform_advanced_search(
                    court=court.canonical_param,
                    order="date",
                    per_page=1,
                )

                oldest_document = SearchResult.create_from_node(
                    search_results.results[0]
                )

                if oldest_document.date:
                    start_year = oldest_document.date.year
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Oldest document: {oldest_document.uri} @ {oldest_document.date.year}"
                        )
                    )
                else:
                    start_year = court.start_year
                    self.stdout.write(
                        self.style.WARNING(
                            f"Couldn't find date of oldest document {oldest_document.uri},\
                                falling back to config value of {court.start_year}"
                        )
                    )

                search_results = perform_advanced_search(
                    court=court.canonical_param,
                    order="-date",
                    per_page=1,
                )

                newest_document = SearchResult.create_from_node(
                    search_results.results[0]
                )

                if newest_document.date:
                    end_year = newest_document.date.year
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Newest document: {newest_document.uri} @ {newest_document.date.year}"
                        )
                    )
                else:
                    end_year = court.end_year
                    self.stdout.write(
                        self.style.WARNING(
                            f"Couldn't find date of newest document {newest_document.uri},\
                                falling back to config value of {court.end_year}"
                        )
                    )

                if start_year < 2000:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Calculated start year of {start_year} seems improbable,\
                                falling back to config value of {court.start_year}"
                        )
                    )
                    start_year = court.start_year

                if end_year > datetime.date.today().year:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Calculated end year of {end_year} is impossible,\
                                falling back to config value of {court.end_year}"
                        )
                    )
                    end_year = court.end_year

                if options["write"]:
                    CourtDates.objects.update_or_create(
                        param=court.canonical_param,
                        defaults={"start_year": start_year, "end_year": end_year},
                    )
                else:
                    self.stdout.write(self.style.NOTICE("Skipping write…"))
            else:
                self.stdout.write(
                    self.style.ERROR(f"{court.name} has no canonical_param! Skipping.")
                )
