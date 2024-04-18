from django import forms
from django.utils.translation import gettext as _

from ds_caselaw_utils import courts as all_courts


class AdvancedSearchForm(forms.Form):
    # TODO: This should become AdvancedSearchQueryForm
    query = forms.CharField(
        required=False,
        label_suffix="",
        widget=forms.TextInput(
            {"placeholder": _("basicsearchform.placeholder"), "id": "search_form"})
        )
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)
    party_name = forms.CharField(required=False)
    judge_name = forms.CharField(required=False)
