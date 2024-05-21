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

    send_text_email_with_smtp_tls(
        from_mail, to_mail, subject, body_text, hostname, port, username, password
    )


def sanitize_value(value):
    sanitized = value
    if isinstance(sanitized, list):
        sanitized = ", ".join(sanitized)
    for remove, replacement in DISALLOWED_CHARACTERS.items():
        sanitized = sanitized.replace(remove, replacement)
    return sanitized


def format_and_sanitize_field(key, value):
    if isinstance(value, dict):
        lines = []
        for key2 in value.keys():
            combined_key = "%s_%s" % (key, key2)
            lines = lines + format_and_sanitize_field(combined_key, value[key2])
        return lines
    elif key == "agent_country":
        return [(key, countries_and_territories_dict().get(value))]
    else:
        return [(key, sanitize_value(value))]


def sanitize_and_format_response_as_xml(form_data):
    lines = []
    for key, value in form_data.items():
        field_lines = format_and_sanitize_field(key, value)
        for key2, sanitized_value in field_lines:
            key2 = key2.replace("_choices", "") if key2.endswith("_choices") else key2
            lines.append(f"<{key2}>{sanitized_value}</{key2}>")
    return "\n".join(lines)


def send_text_email_with_smtp_tls(
    from_mail, to_mail, subject, body_text, hostname, port, username, password
):
    msg = MIMEMultipart()
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Subject"] = subject
    msg.attach(MIMEText(body_text, "plain"))
    server = smtplib.SMTP(hostname, port)
    server.starttls()
    server.login(username, password)
    server.sendmail(from_mail, to_mail, msg.as_string())
    server.quit()
