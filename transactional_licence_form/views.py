from django.views.generic import TemplateView


class FormView(TemplateView):
    template_name = "form.html"
