from factory.django import DjangoModelFactory

from judgments.models import CourtDates


class CourtDateFactory(DjangoModelFactory):
    class Meta:
        model = CourtDates

    param = "uksc"
    start_year = 2001
    end_year = 2024
