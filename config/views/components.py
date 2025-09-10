from django.views.generic import TemplateView


class ComponentsView(TemplateView):
    template_engine = "jinja"
    template_name = "pages/components.jinja"
