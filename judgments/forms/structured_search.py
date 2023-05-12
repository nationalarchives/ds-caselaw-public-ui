from django import forms
from django.utils.translation import ugettext_lazy
from ds_caselaw_utils import courts


class DateInput(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(), forms.TextInput(), forms.TextInput()]
        super(DateInput, self).__init__(widgets, attrs)


class DateField(forms.MultiValueField):
    widget = DateInput

    def __init__(self, **kwargs):
        fields = [forms.CharField(), forms.CharField(), forms.CharField()]
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, values):
        return "-".join(values)


def court_select_choices():
    return [(c.canonical_param, c.name) for c in courts.get_selectable()]


class StructuredSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "id": "search_term",
                "class": "search-term-component__search-term-input",
                "placeholder": ugettext_lazy("basicsearchform.cta"),
            }
        ),
    )
    neutral_citation = forms.CharField(
        required=False,
        label="Neutral citation",
        widget=forms.TextInput(
            attrs={
                "class": "structured-search__limit-to-input",
                "aria-describedby": "neutral_citation-help-text",
            }
        ),
    )
    specific_keyword = forms.CharField(
        required=False,
        label="Containing specific keywords",
        widget=forms.TextInput(
            attrs={
                "class": "structured-search__limit-to-input",
                "aria-describedby": "specific_keyword-help-text",
            }
        ),
    )
    court = forms.MultipleChoiceField(
        required=False,
        choices=court_select_choices(),
        widget=forms.CheckboxSelectMultiple,
        label="From specific courts or tribunals",
    )
    from_date = DateField(required=False, label="From date")
    to_date = DateField(required=False, label="To date")
    party = forms.CharField(
        required=False,
        label="Party name",
        widget=forms.TextInput(
            attrs={
                "class": "structured-search__limit-to-input",
                "aria-describedby": "party_name-help-text",
            }
        ),
    )
    judge = forms.CharField(
        required=False,
        label="Judge name",
        widget=forms.TextInput(
            attrs={
                "class": "structured-search__limit-to-input",
                "aria-describedby": "judge_name-help-text",
            }
        ),
    )
