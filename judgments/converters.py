import datetime

court_regex = "ewhc|uksc|ukpc|ewca|ewcop|ewfc|ukut|eat|ukftt"
subdivision_regex = "civ|crim|admin|admlty|ch|comm|costs|fam|ipec|mercantile|pat|qb|kb|iac|lc|tcc|aac|scco|tc|grc"
year_regex = "[0-9]{4}"
id_regex = "[0-9]+"


class JudgmentConverter:
    regex = f"(?:{court_regex})(?:/(?:{subdivision_regex}))?/{year_regex}/{id_regex}"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


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
