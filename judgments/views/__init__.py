import re


def trim_leading_slash(uri):
    return re.sub("^/|/$", "", uri)
