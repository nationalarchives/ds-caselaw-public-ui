import datetime


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
    regex = "ewhc|uksc|ukpc|ewca|ewcop|ewfc|ukut|eat"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class SubdivisionConverter:
    regex = "civ|crim|admin|admlty|ch|comm|costs|fam|ipec|mercantile|pat|qb|iac|lc|tcc|aac|scco"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
