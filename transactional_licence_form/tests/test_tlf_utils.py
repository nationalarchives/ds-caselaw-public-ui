import unittest
from unittest import mock

from transactional_licence_form import utils
from transactional_licence_form.tests import fixtures


class TestTLFUtils(unittest.TestCase):
    @mock.patch("transactional_licence_form.utils.settings")
    @mock.patch("transactional_licence_form.utils.EmailSender.__new__")
    @mock.patch("transactional_licence_form.utils.sanitize_and_format_response_as_xml")
    def test_send_form_response(self, mock_sanitize, mock_email_sender, mock_settings):
        # Setup fixtures:
        from_email = "from@example.com"
        delivery_email = "delivery@example.com"
        email_subject = "email subject"
        ses_username = "smtp_username"
        ses_password = "smtp_password"
        ses_server = "smtp_server"
        ses_port = 1234
        sanitized_text = "sanitized text"
        form_data = {"test_form_data": "test"}
        # Mock the django settings
        mock_settings.TRANSACTIONAL_LICENCE_FROM_EMAIL = from_email
        mock_settings.TRANSACTIONAL_LICENCE_DELIVERY_EMAIL = delivery_email
        mock_settings.TRANSACTIONAL_LICENCE_EMAIL_SUBJECT = email_subject
        mock_settings.SES_SMTP_USERNAME = ses_username
        mock_settings.SES_SMTP_PASSWORD = ses_password
        mock_settings.SES_SMTP_SERVER = ses_server
        mock_settings.SES_SMTP_PORT = ses_port
        # Mock sanitize and send method calls
        mock_sanitize.return_value = sanitized_text
        mock_email_sender.return_value = mock_email_sender
        mock_email_sender.__enter__.return_value = mock_email_sender

        # Actually exercise the method
        utils.send_form_response_to_dynamics(form_data)

        # Assert that the form data is sanitized
        mock_sanitize.assert_called_with(form_data)
        # Assert that the email sender is instantiated correctly.
        mock_email_sender.assert_called_with(utils.EmailSender, ses_server, ses_port, ses_username, ses_password)
        # Assert that the email is sent.
        mock_email_sender.__enter__.assert_called()
        mock_email_sender.send_mail.assert_called_with(from_email, delivery_email, email_subject, sanitized_text)
        # Assert that the sender is torn down correctly
        mock_email_sender.__exit__.assert_called()

    def test_sanitize_and_format_response_as_xml(self):
        """
        Tests:
            - that the form data fields are correctly mapped to the tags expected in the CRM system,
            - that country names are correctly resolved (agent_country)
            - That the licence holder contact is correctly defaulted i
                (licence_holder_email, licence_holder_lastname)
            - That angle brackets are correctly escaped (agent_companyname)
        """

        actual_result = utils.sanitize_and_format_response_as_xml(fixtures.FORM_DATA)
        self.assertEqual(fixtures.EXPECTED_SANITIZED_RESULT, actual_result)
