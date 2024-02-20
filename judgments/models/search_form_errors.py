from collections import defaultdict


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
