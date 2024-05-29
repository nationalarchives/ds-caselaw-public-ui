from django.forms import CheckboxSelectMultiple


class CheckBoxSelectCourtWithYearRange(CheckboxSelectMultiple):
    """
    Override the default CheckBoxSelectMultiple option template
    to allow us to use templatetags to render year ranges for courts.
    """

    option_template_name = "forms/widgets/court_input_option_with_years.html"
    template_name = "forms/widgets/court_multiple_input.html"
