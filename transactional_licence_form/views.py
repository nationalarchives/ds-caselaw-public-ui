from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from formtools.wizard.views import NamedUrlSessionWizardView

from .forms import FORMS
from .utils import send_form_response_to_dynamics

TEMPLATE_OVERRIDES = {
    "review": "review.html",
    "nine-principles-1": "nine_principles_1.html",
}


class FormWizardView(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATE_OVERRIDES.get(self.steps.current, "form.html")]

    def render_goto_step(self, goto_step, **kwargs):
        # We override this to ensure that the "reviewing" state is passed along.
        self.storage.current_step = goto_step
        url = self.get_step_url(goto_step)
        if self.in_review():
            self.request.session["transactional_licence_form_reviewing"] = True
        return redirect(url)

    def in_review(self):
        has_review_parameter = bool(
            self.request.session.get("transactional_licence_form_reviewing", False)
            or self.request.POST.get("reviewing", False)
        )
        return has_review_parameter and self.steps.current != "review"

    def get_all_cleaned_data_by_form(self):
        cleaned_data = {}
        for form_key in self.get_form_list():
            cleaned_data[form_key] = {}
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    cleaned_data[form_key].update(
                        {"formset-%s" % form_key: form_obj.cleaned_data}
                    )
                else:
                    cleaned_data[form_key].update(form_obj.cleaned_data)
        return cleaned_data

    def get_all_field_names(self):
        field_names = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
            for field in form_obj:
                field_names.update({field.name: field.label})
        return field_names

    def get_all_form_titles(self):
        form_titles = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
            form_titles.update({form_key: form_obj.title})
        return form_titles

    def get_context_data(self, form, **kwargs):
        context = super(FormWizardView, self).get_context_data(form)
        context["all_data"] = self.get_all_cleaned_data_by_form()
        context["all_field_names"] = self.get_all_field_names()
        context["all_form_titles"] = self.get_all_form_titles()
        context["reviewing"] = self.in_review()
        return context

    def done(self, form_list, **kwargs):
        del self.request.session["transactional_licence_form_reviewing"]
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

    def post(self, _request, *_args, **_kwargs):
        # TODO Tim handle the logic for the 'pre-applcation check' step here.
        pass


def wizard_view(url_name):
    return FormWizardView.as_view(
        FORMS,
        url_name=url_name,
        done_step_name="submitted",
    )
