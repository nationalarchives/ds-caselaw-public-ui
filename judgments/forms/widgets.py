from django.forms import CheckboxSelectMultiple


class CheckBoxSelectCourtWithYearRange(CheckboxSelectMultiple):
    option_template_name = "forms/widgets/court_input_option_with_years.html"
 