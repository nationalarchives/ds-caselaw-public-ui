from django.forms import CheckboxSelectMultiple
from django.template import engines


class CheckBoxSelectCourtWithYearRange(CheckboxSelectMultiple):
    """
    Override the default CheckBoxSelectMultiple option template
    to allow us to use templatetags to render year ranges for courts.
    """

    option_template_name = "forms/widgets/court_input_option_with_years.jinja"
    template_name = "forms/widgets/court_multiple_input.jinja"

    def _render(self, template_name, context, renderer=None):
        jinja_engine = engines["jinja"]
        template = jinja_engine.get_template(template_name)

        return template.render(context)
