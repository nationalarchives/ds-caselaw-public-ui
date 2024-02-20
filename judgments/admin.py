from django.contrib import admin

from judgments.models.court_dates import CourtDates


@admin.register(CourtDates)
class CourtDatesAdmin(admin.ModelAdmin):
    pass
