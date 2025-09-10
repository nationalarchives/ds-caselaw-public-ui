import datetime
import itertools

from ds_caselaw_utils import courts


def converter_regexes(court_repo) -> tuple[str, str]:
    """Return regex like "uksc|ukftt" (court) and "crim|civ" (subdivision) suitable for URL parsing"""
    params = tuple(itertools.chain.from_iterable([court.param_aliases for court in court_repo.get_all()]))
    court_set = set([court for param in params if (court := param.partition("/")[0])])
    subdivision_set = set([subdivision for param in params if (subdivision := param.partition("/")[2])])
    court_regex = "|".join(sorted(court_set))
    subdivision_regex = "|".join(sorted(subdivision_set))
    return (court_regex, subdivision_regex)


court_regex, subdivision_regex = converter_regexes(courts)


class YearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value


class DateConverter:
    regex = "([0-9]{4})-([0-9]{2})-([0-9]{2})"

    def to_python(self, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d")

    def to_url(self, value):
        if value is None:
            raise ValueError

        return value.strftime("%Y-%m-%d")


class CourtConverter:
    regex = court_regex

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class SubdivisionConverter:
    regex = subdivision_regex

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class FileFormatConverter:
    regex = "data.pdf|generated.pdf|data.xml|data.html"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class DocumentUriConverter:
    regex = r"[a-z0-9./-]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class ComponentConverter:
    regex = "press-summary"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
