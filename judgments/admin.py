from django.contrib import admin

from judgments.models import CourtDates


@admin.register(CourtDates)
class CourtDatesAdmin(admin.ModelAdmin):
    pass
