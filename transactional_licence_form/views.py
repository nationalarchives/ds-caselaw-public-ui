from django.shortcuts import render
from django.views.generic import TemplateView
from formtools.wizard.views import NamedUrlSessionWizardView

from .forms import FORMS
from .utils import send_form_response_to_dynamics

TEMPLATE_OVERRIDES = {"review": "review.html"}


class FormWizardView(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATE_OVERRIDES.get(self.steps.current, "form.html")]

    def get_context_data(self, form, **kwargs):
        context = super(FormWizardView, self).get_context_data(form)
        context["all_data"] = self.get_all_cleaned_data()
        return context

    def done(self, form_list, **kwargs):
        send_form_response_to_dynamics(self.get_all_cleaned_data())
        return render(self.request, "submitted.html")


class StartView1(TemplateView):
    template_name = "start.html"


class StartView2(TemplateView):
    template_name = "start2.html"


class StartView3(TemplateView):
    template_name = "start3.html"


def wizard_view(url_name):
    return FormWizardView.as_view(
        FORMS,
        url_name=url_name,
        done_step_name="submitted",
    )
