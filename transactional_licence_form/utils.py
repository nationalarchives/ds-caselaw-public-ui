import functools
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

DISALLOWED_CHARACTERS = {"<": "&lt;", ">": "&gt;"}

COUNTRIES_AND_TERRITORIES_JSON_PATH = (
    "ds_judgements_public_ui/static/js/location-autocomplete-canonical-list.json"
)


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


def format_and_sanitize_field(key, value):
    if isinstance(value, dict):
        return format_and_sanitize_composite_field(key, value)
    elif key == "agent_country":
        return [(key, countries_and_territories_dict().get(value))]
    else:
        return [(key, sanitize_value(value))]


def format_and_sanitize_composite_field(key, value):
    lines = []
    for key2 in value.keys():
        combined_key = "%s_%s" % (key, key2)
        lines = lines + format_and_sanitize_field(combined_key, value[key2])
    return lines


def sanitize_and_format_response_as_xml(form_data):
    lines = []
    for key, value in form_data.items():
        field_lines = format_and_sanitize_field(key, value)
        for key2, sanitized_value in field_lines:
            xml_key = xml_key_for(key2)
            lines.append(f"<{xml_key}>{sanitized_value}</{xml_key}>")
    return "\n".join(lines)


def xml_key_for(key):
    return key.replace("_choices", "") if key.endswith("_choices") else key
