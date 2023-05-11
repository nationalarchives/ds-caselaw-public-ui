from collections import defaultdict

from django.db import models
from django.db.models import Max, Min


class CourtDates(models.Model):
    class Meta:
        verbose_name = "court date range"
        verbose_name_plural = "court date ranges"

    param = models.CharField(max_length=64, primary_key=True)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(blank=False)

    @staticmethod
    def min_year():
        result = CourtDates.objects.aggregate(Min("start_year"))
        return result["start_year__min"]

    @staticmethod
    def max_year():
        result = CourtDates.objects.aggregate(Max("end_year"))
        return result["end_year__max"]


class SearchFormErrors:
    def __init__(self):
        self.messages = []
        self.fields = defaultdict(list)

    def has_errors(self, field=None):
        if field is None:
            return len(self.messages) > 0 and len(self.fields.keys()) > 0
        else:
            return len(self.fields[field])

    def add_error(self, message, field=None, fieldMessage=None):
        self.messages.append(message)
        if field is not None:
            self.fields[field].append(fieldMessage)
