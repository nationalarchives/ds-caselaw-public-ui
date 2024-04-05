from django.shortcuts import render
from django.views.generic import TemplateView
from formtools.wizard.views import NamedUrlSessionWizardView

from . import forms


class FormWizardView(NamedUrlSessionWizardView):
    template_name = "form.html"

    def done(self, form_list, **kwargs):
        return render(self.request, "review.html", {"forms": form_list})

    template_name = "form.html"


class StartView(TemplateView):
    template_name = "start.html"


def wizard_view(url_name):
    return FormWizardView.as_view(
        forms.FORMS,
        url_name=url_name,
        done_step_name="review",
    )
