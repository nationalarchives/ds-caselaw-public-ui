import re


def capfirst(value):
    if not value:
        return value
    return value[0].upper() + value[1:]


def hyphenate(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-")
