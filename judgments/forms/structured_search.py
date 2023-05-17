from calendar import monthrange
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from flags.state import flag_enabled
from ds_caselaw_utils import courts
class DateInput(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(), forms.TextInput(), forms.TextInput()]
        super(DateInput, self).__init__(widgets, attrs)


class DateField(forms.MultiValueField):
    widget = DateInput

    def __init__(self, default_to_last=False, **kwargs):
        self.default_to_last = default_to_last
        fields = [
            forms.IntegerField(required=False),
            forms.IntegerField(required=False, min_value=1, max_value=12,
                               error_messages={
                                   'max_value': 'Month must be less than 12',
                                   'min_value': 'Month must be greater than 1',
                                   'invalid': "Please enter a number"
                               }),
            forms.IntegerField(required=False, min_value=1, max_value=31)
        ]
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, values):
        if len(values) > 0:
            year = values[0]
            if year:
                default_month = 12 if self.default_to_last else 1
                month = values[1] or default_month
                default_day = monthrange(year, month)[1] if self.default_to_last    else 1
                day = values[2] or default_day
                try:
                    dt = datetime(year, month, day)
                    return dt.strftime("%Y-%m-%d")
                except ValueError as err:
                    raise ValidationError(err.args[0])



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
