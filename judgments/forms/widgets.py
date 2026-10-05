from django.forms import CheckboxSelectMultiple
from django.template import engines


class CheckBoxSelectCourtWithYearRange(CheckboxSelectMultiple):
    """
    Override the default CheckBoxSelectMultiple option template
    to allow us to use templatetags to render year ranges for courts.
    """

    option_template_name = "forms/widgets/court_input_option_with_years.jinja"
    template_name = "forms/widgets/court_multiple_input.jinja"

    def __init__(self, *args, court_group_count=None, **kwargs):
        self.court_group_count = court_group_count
        super().__init__(*args, **kwargs)
        if court_group_count is not None:
            self.template_name = "forms/widgets/court_and_tribunal_input.jinja"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        groups = context["widget"]["optgroups"]
        context["court_groups"] = groups[: self.court_group_count]
        context["tribunal_groups"] = groups[self.court_group_count :]
        return context

    def _render(self, template_name, context, renderer=None):
        jinja_engine = engines["jinja"]
        template = jinja_engine.get_template(template_name)

        return template.render(context)
