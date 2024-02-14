class SchemaFileConverter:
    regex = r"(?:xml|caselaw|akn-modified)\.xsd"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
