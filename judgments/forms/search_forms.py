from typing import Optional, Union

from django import forms
from django.forms import ValidationError
from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import CourtGroup, CourtParam

from judgments.utils import preprocess_query

from .fields import DateRangeInputField
from .widgets import CheckBoxSelectCourtWithYearRange

court_choices_dict = dict[Union[Optional[str], CourtParam], Union[str, dict[CourtParam, str]]]


def _get_choices_by_group(courts: list[CourtGroup]):
    """
    Given a list of court objects, construct a dictionary containing
    {"key1": "value1"} for non-grouped courts, and {"court_group": {"key1": "value1"}}
    for grouped courts. This allows us to nest choices within groups when rendering
    a `MultipleChoiceField` field in Django.

    e.g.
    {
        "court_group_1": {"key1": "value1"},
        "key2": "value2"
    }
    """
    options: court_choices_dict = {}
    for group in courts:
        if group.display_heading:
            court_group: court_choices_dict = {
                group.name: {
                    court.canonical_param: court.grouped_name for court in group.courts if court.canonical_param
                }
            }
            options = options | court_group
        else:
            isolated_court: court_choices_dict = {
                court.canonical_param: court.grouped_name for court in group.courts if court.canonical_param
            }
            options = options | isolated_court
    return options


COURT_CHOICES = _get_choices_by_group(all_courts.get_grouped_selectable_courts())
TRIBUNAL_CHOICES = _get_choices_by_group(all_courts.get_grouped_selectable_tribunals())


class CourtOrTribunalField(forms.MultipleChoiceField):
    def _get_short_identifiers(self) -> set[str]:
        all_shorts: set[str] = set()
        for key, value in self.choices:
            if isinstance(value, list):
                all_shorts = all_shorts | set(x[0].partition("/")[0] for x in value)
        return all_shorts

    def validate(self, *args, **kwargs):
        short_identifiers = self._get_short_identifiers()
        try:
            return super().validate(*args, **kwargs)
        except ValidationError as e:
            if e.params and e.params.get("value") in short_identifiers:
                return None  # signal that this is an acceptable value
            else:
                raise


class AdvancedSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": "Search...",
                "id": "search_form",
                "class": "search-term-component__search-term-input",
            }
        ),
    )
    # Validation for multi-field fields such as `DateInputField` is done on the sub fields
    from_date = DateRangeInputField(
        label="From Date",
        help_text="For example <em>01 01 2003</em> or <em>2003</em>",
        require_all_fields=False,
        required=False,
        date_type="from",
    )
    to_date = DateRangeInputField(
        label="To Date",
        help_text="For example <em>30 04 2023</em> or <em>2023</em>",
        require_all_fields=False,
        required=False,
        date_type="to",
    )
    # Courts and tribunals are split here because it's easier to render
    # them and then recombine in the view for querying MarkLogic
    court = CourtOrTribunalField(
        choices=COURT_CHOICES,
        widget=CheckBoxSelectCourtWithYearRange(),
        label="From specific courts or tribunals",
        required=False,
    )

    tribunal = CourtOrTribunalField(
        choices=TRIBUNAL_CHOICES,
        widget=CheckBoxSelectCourtWithYearRange(),
        required=False,
    )

    party = forms.CharField(
        widget=forms.TextInput(
            {
                "class": "structured-search__limit-to-input",
            }
        ),
        required=False,
    )
    judge = forms.CharField(
        widget=forms.TextInput(
            {
                "class": "structured-search__limit-to-input",
            }
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        # Validate that from is before to now that we have access to both fields
        if cleaned_data is None:  # make the type checker happier
            raise RuntimeError("Cleaned data can never be None, this should never occur")
        to_date = cleaned_data.get("to_date")
        from_date = cleaned_data.get("from_date")
        if from_date and to_date:
            if from_date > to_date:
                raise ValidationError(
                    "Please enter a 'to' date after the 'from' date",
                    code="to_date",
                )
        # Run the pre-process query step
        # Ignore warnings related to MyPy not understanding what cleaned_data is
        if cleaned_data.get("query"):
            cleaned_data["query"] = preprocess_query(cleaned_data.get("query", ""))
        for parameter in ["query", "from_date", "to_date", "court", "tribunal", "party", "judge"]:
            if cleaned_data.get(parameter, "Non-nilsy placeholder") in (None, "", []):
                del cleaned_data[parameter]
        return cleaned_data
