from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from formtools.wizard.forms import ManagementForm
from formtools.wizard.views import NamedUrlSessionWizardView

from .forms import FORMS
from .utils import send_form_response_to_dynamics

TEMPLATE_OVERRIDES = {
    "contact": "contact.html",
    "review": "review.html",
    "nine-principles-1": "nine_principles_1.html",
    "nine-principles-2": "nine_principles_2.html",
    "organization": "organization.html",
    "project-purpose": "project-purpose.html",
    "public-statement": "public-statement.html",
}

REVIEWING_SESSION_KEY = "transactional_licence_form_reviewing"


class FormWizardView(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATE_OVERRIDES.get(self.steps.current, "form.html")]

    def render_goto_step(self, goto_step, **kwargs):
        # We override this to ensure that the "reviewing" state is passed along.
        self.storage.current_step = goto_step
        url = self.get_step_url(goto_step)
        if self.in_review():
            self.request.session[REVIEWING_SESSION_KEY] = True
        return redirect(url)

    def post(self, *args, **kwargs):
        # We override this to ensure that the form is saved when returning to the review page

        wizard_goto_step = self.request.POST.get("wizard_goto_step", None)
        if not self.in_review():
            # If we are not reviewing, we follow the default behaviour: we do not validate or save the form
            # and go directly to the step.
            if wizard_goto_step and wizard_goto_step in self.get_form_list():
                return self.render_goto_step(wizard_goto_step)

        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise SuspiciousOperation(
                "ManagementForm data is missing or has been tampered."
            )

        form_current_step = management_form.cleaned_data["current_step"]
        if (
            form_current_step != self.steps.current
            and self.storage.current_step is not None
        ):
            self.storage.current_step = form_current_step

        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        if form.is_valid():
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(
                self.steps.current, self.process_step_files(form)
            )

            if self.steps.current == self.steps.last:
                return self.render_done(form, **kwargs)
            else:
                if wizard_goto_step and wizard_goto_step in self.get_form_list():
                    # If we are reviewing, and there is a goto step, we go to that step.
                    return self.render_goto_step(wizard_goto_step)
                else:
                    # Otherwise we follow the default behaviour.
                    return self.render_next_step(form)
        return self.render(form)

    def in_review(self):
        has_review_parameter = bool(
            self.request.session.get(REVIEWING_SESSION_KEY, False)
            or self.request.POST.get("reviewing", False)
        )
        return has_review_parameter and self.steps.current != "review"

    def get_form_object(self, form_key):
        return self.get_form(
            step=form_key,
            data=self.storage.get_step_data(form_key),
            files=self.storage.get_step_files(form_key),
        )

    def get_all_cleaned_data_by_form(self):
        cleaned_data = {}
        for form_key in self.get_form_list():
            cleaned_data[form_key] = {}
            form_obj = self.get_form_object(form_key)
            if form_obj.is_valid() and isinstance(form_obj.cleaned_data, (tuple, list)):
                cleaned_data[form_key].update(
                    {"formset-%s" % form_key: form_obj.cleaned_data}
                )
            elif form_obj.is_valid():
                cleaned_data[form_key].update(form_obj.cleaned_data)
        return cleaned_data

    def get_all_field_names(self):
        field_names = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form_object(form_key)
            for field in form_obj:
                field_names.update({field.name: field.label})
        return field_names

    def get_all_forms(self):
        all_forms = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form_object(form_key)
            all_forms.update({form_key: form_obj})
        return all_forms

    def get_context_data(self, form, **kwargs):
        context = super(FormWizardView, self).get_context_data(form)
        context["all_data"] = self.get_all_cleaned_data_by_form()
        context["all_field_names"] = self.get_all_field_names()
        context["all_forms"] = self.get_all_forms()
        context["reviewing"] = self.in_review()
        return context

    def done(self, form_list, **kwargs):
        if REVIEWING_SESSION_KEY in self.request.session:
            del self.request.session[REVIEWING_SESSION_KEY]
        send_form_response_to_dynamics(self.get_all_cleaned_data())
        return render(self.request, "submitted.html")


class StartView1(TemplateView):
    template_name = "start.html"


class StartView2(TemplateView):
    template_name = "start2.html"


class StartView3(TemplateView):
    template_name = "start3.html"


class DownloadView(TemplateView):
    template_name = "download.html"


class ConfirmationView(TemplateView):
    template_name = "confirmation.html"


def wizard_view(url_name):
    return FormWizardView.as_view(
        FORMS,
        url_name=url_name,
        done_step_name="submitted",
    )
