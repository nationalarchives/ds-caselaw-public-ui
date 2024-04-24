import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DISALLOWED_CHARACTERS = {"<": "&lt;", ">": "&gt;"}

COUNTRIES_AND_TERRITORIES_JSON_PATH = (
    "ds_judgements_public_ui/static/js/location-autocomplete-canonical-list.json"
)


def countries_and_territories():
    with open(COUNTRIES_AND_TERRITORIES_JSON_PATH) as file:
        return [(pair[1], pair[0]) for pair in json.load(file)]


def send_form_response_to_dynamics(form_data):
    from_mail = os.environ["TRANSACTIONAL_LICENCE_FROM_EMAIL"]
    to_mail = os.environ["TRANSACTIONAL_LICENCE_DELIVERY_EMAIL"]
    subject = os.environ["TRANSACTIONAL_LICENCE_EMAIL_SUBJECT"]
    username = os.environ["SES_SMTP_USERNAME"]
    password = os.environ["SES_SMTP_PASSWORD"]
    hostname = os.environ["SES_SMTP_SERVER"]
    port = os.environ["SES_SMTP_PORT"]

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


def sanitize_and_format_response_as_xml(form_data):
    lines = []
    for key, value in form_data.items():
        sanitized = sanitize_value(value)
        lines.append(f"<{key}>{sanitized}</{key}>")
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
    server.quit
