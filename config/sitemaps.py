from django.contrib import sitemaps
from django.urls import reverse
from ds_caselaw_utils import courts


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ["home", "about_this_service", "what_to_expect", "courts_and_tribunals"]

    def location(self, item):
        return reverse(item)


class CourtsSitemap(sitemaps.Sitemap):
    def items(self):
        court_codes = []
        for court_group in courts.get_listable_groups():
            court_codes += court_group.courts
        return court_codes

    def location(self, item):
        return reverse("court_or_tribunal", kwargs={"param": item.canonical_param})


class CourtSitemap(sitemaps.Sitemap):
    """This is a 'fake' sitemap to trick the sitemaps framework into passing requests to the dynamic view."""

    pass
