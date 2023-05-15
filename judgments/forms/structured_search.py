from calendar import monthrange
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ds_caselaw_utils import courts
class DateInput(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(), forms.TextInput(), forms.TextInput()]
        super(DateInput, self).__init__(widgets, attrs)


class DateField(forms.MultiValueField):
    widget = DateInput

    def __init__(self, default_to_last=False, **kwargs):
        fields = [forms.IntegerField(), forms.IntegerField(), forms.IntegerField()]
        self.default_to_last = default_to_last
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, values):
        errors = []
        def get_value_as_int(i, default=None):
            if values[i] and len(values[i]) > 0:
                try:
                    return int(values[i])
                except ValueError:
                    errors.append(ValidationError("please enter a number"))
            else:
                return default
        year = get_value_as_int(0)
        if year is not None:
            default_month = 12 if self.default_to_last else 1
            month = get_value_as_int(1, default_month)
            default_day = monthrange(year, month)[1] if self.default_to_last    else 1
            day = get_value_as_int(2, default_day)
            dt = datetime(year, month, day)
        if any(errors):
            raise ValidationError(errors)
        return dt.strftime("%Y-%m-%d")


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
                "placeholder": _("basicsearchform.cta"),
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
