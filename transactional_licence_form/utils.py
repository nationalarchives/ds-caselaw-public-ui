import functools
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.template.loader import render_to_string

DISALLOWED_CHARACTERS = {"<": "&lt;", ">": "&gt;"}

COUNTRIES_AND_TERRITORIES_JSON_PATH = (
    "ds_judgements_public_ui/static/js/location-autocomplete-canonical-list.json"
)

EMAIL_TEMPLATE_PATH = "dynamics_email_template.txt"


class EmailSender:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.server = smtplib.SMTP(self.hostname, self.port)

    def __enter__(self):
        self.server.starttls()
        self.server.login(self.username, self.password)
        return self

    def __exit__(self, *args, **kwargs):
        self.server.quit()

    def send_mail(self, from_mail, to_mail, subject, body_text):
        msg = MIMEMultipart()
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))
        self.server.sendmail(from_mail, to_mail, msg.as_string())


def list_to_choices(values):
    return [(v, v) for v in values]


@functools.lru_cache(maxsize=1)
def countries_and_territories_dict():
    with open(COUNTRIES_AND_TERRITORIES_JSON_PATH) as file:
        return dict([(pair[1], pair[0]) for pair in json.load(file)])


def countries_and_territories_choices():
    return list(countries_and_territories_dict().items())


def send_form_response_to_dynamics(form_data):
    from_mail = settings.TRANSACTIONAL_LICENCE_FROM_EMAIL
    to_mail = settings.TRANSACTIONAL_LICENCE_DELIVERY_EMAIL
    subject = settings.TRANSACTIONAL_LICENCE_EMAIL_SUBJECT
    username = settings.SES_SMTP_USERNAME
    password = settings.SES_SMTP_PASSWORD
    hostname = settings.SES_SMTP_SERVER
    port = settings.SES_SMTP_PORT

    body_text = sanitize_and_format_response_as_xml(form_data)

    with EmailSender(hostname, port, username, password) as sender:
        sender.send_mail(from_mail, to_mail, subject, body_text)


def sanitize_value(value):
    sanitized = value
    if isinstance(sanitized, list):
        sanitized = ", ".join(sanitized)
    for remove, replacement in DISALLOWED_CHARACTERS.items():
        sanitized = sanitized.replace(remove, replacement)
    return sanitized


def sanitize_and_format_response_as_xml(form_data):
    sanitized_fields = {}
    for key, value in form_data.items():
        if isinstance(value, dict):
            for key2, value2 in value.items():
                sanitized_fields[f"{key}_{key2}"] = sanitize_value(value2)
        else:
            sanitized_fields[key] = sanitize_value(value)
    return render_to_string(EMAIL_TEMPLATE_PATH, sanitized_fields)
