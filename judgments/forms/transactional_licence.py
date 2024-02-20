import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django import forms
from django.shortcuts import render
from django.template.loader import render_to_string
from formtools.wizard.views import NamedUrlSessionWizardView


class Form1(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


class Form2(forms.Form):
    name = forms.CharField()


class TransactionalLicenceWizard(NamedUrlSessionWizardView):

    def done(self, form_list, form_dict, **kwargs):
        form_data = dict()
        for key, form in form_dict.items():
            for key2, value in form.cleaned_data.items():
                form_data["%s_%s" % (key, key2)] = value
        xml_data = render_to_string("transactional_licence/email.xml", form_data)
        msg = MIMEMultipart()
        from_mail = os.environ["TRANSACTIONAL_LICENCE_FROM_EMAIL"]
        to_mail = os.environ["TRANSACTIONAL_LICENCE_DELIVERY_EMAIL"]
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg["Subject"] = os.environ["TRANSACTIONAL_LICENCE_EMAIL_SUBJECT"]
        msg.attach(MIMEText(xml_data, "plain"))
        server = smtplib.SMTP(
            os.environ["SES_SMTP_SERVER"], int(os.environ["SES_SMTP_PORT"])
        )
        server.starttls()
        server.login(os.environ["SES_SMTP_USERNAME"], os.environ["SES_SMTP_PASSWORD"])
        server.sendmail(from_mail, to_mail, msg.as_string())
        server.quit
        return render(
            self.request, "transactional_licence/done.html", {"form_data": form_data}
        )


def wizard_view(url_name):
    return TransactionalLicenceWizard.as_view(
        (("contact", Form1), ("organization", Form2)),
        url_name=url_name,
        done_step_name="finished",
    )
