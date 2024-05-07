from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext as _
from ds_caselaw_utils import courts as all_courts

from judgments.utils import preprocess_query

from .fields import DateRangeInputField
from .widgets import CheckBoxSelectCourtWithYearRange


def _get_choices_by_group(courts):
    options: dict = {}
    for group in courts:
        if group.display_heading:
            option = {
                group.name: {
                    court.canonical_param: court.grouped_name for court in group.courts
                }
            }
        else:
            option = {
                court.canonical_param: court.grouped_name for court in group.courts
            }
        options = options | option
    return options


COURT_CHOICES = _get_choices_by_group(all_courts.get_grouped_selectable_courts())
TRIBUNAL_CHOICES = _get_choices_by_group(all_courts.get_grouped_selectable_tribunals())


class AdvancedSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": _("basicsearchform.placeholder"),
                "id": "search_form",
                "class": "search-term-component__search-term-input",
            }
        ),
    )
    # Validation for multi-field fields such as `DateInputField` is done on the sub fields
    from_date = DateRangeInputField(
        label=_("From Date"),
        help_text=_("For example <em>01 01 2003</em> or <em>2003</em>"),
        require_all_fields=False,
        required=False,
        date_type="from",
    )
    to_date = DateRangeInputField(
        label=_("To Date"),
        help_text=_("For example <em>30 04 2023</em> or <em>2023</em>"),
        require_all_fields=False,
        required=False,
        date_type="to",
    )
    # Courts and tribunals are split here because it's easier to render
    # them and then recombine in the view for querying MarkLogic
    courts = forms.MultipleChoiceField(
        choices=COURT_CHOICES,
        widget=CheckBoxSelectCourtWithYearRange(),
        label="From specific courts or tribunals",
        required=False,
    )
    tribunals = forms.MultipleChoiceField(
        choices=TRIBUNAL_CHOICES,
        widget=CheckBoxSelectCourtWithYearRange(),
        required=False,
    )
    party_name = forms.CharField(
        widget=forms.TextInput(
            {
                "class": "structured-search__limit-to-input",
            }
        ),
        required=False,
    )
    judge_name = forms.CharField(
        widget=forms.TextInput(
            {
                "class": "structured-search__limit-to-input",
            }
        ),
        required=False,
    )

    def clean(self):
        # Validate that from is before to now that we have access to both fields
        cleaned_data = super().clean()
        to_date = cleaned_data.get("to_date", None)
        from_date = cleaned_data.get("from_date", None)
        if from_date and to_date:
            if from_date > to_date:
                raise ValidationError(
                    _("To date must be after from date"),
                    code="to_date",
                )
        # Run the pre-process query steps
        cleaned_data["query"] = preprocess_query(cleaned_data["query"])
        return cleaned_data
