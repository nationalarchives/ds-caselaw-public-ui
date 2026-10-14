from judgments.search_scopes import SEARCH_SCOPE_LABELS


def get_scope_label(value):
    if isinstance(value, list):
        return ", ".join(
            SEARCH_SCOPE_LABELS[scope] for scope in value if scope in SEARCH_SCOPE_LABELS and scope != "all_courts"
        )
    if value != "all_courts":
        return SEARCH_SCOPE_LABELS.get(value)
