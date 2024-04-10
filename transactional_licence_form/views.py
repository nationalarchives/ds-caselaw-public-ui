from django.shortcuts import render
from django.views.generic import TemplateView
from formtools.wizard.views import NamedUrlSessionWizardView

from . import forms

TEMPLATE_OVERRIDES = {"review": "review.html"}


class FormWizardView(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATE_OVERRIDES.get(self.steps.current, "form.html")]

    def get_context_data(self, form, **kwargs):
        context = super(FormWizardView, self).get_context_data(form)
        context["all_data"] = self.get_all_cleaned_data()
        return context

    def done(self, form_list, **kwargs):
        return render(self.request, "submitted.html")


class StartView(TemplateView):
    template_name = "start.html"


def wizard_view(url_name):
    return FormWizardView.as_view(
        forms.FORMS,
        url_name=url_name,
        done_step_name="submitted",
    )
