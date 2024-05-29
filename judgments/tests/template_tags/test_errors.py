from django.test import TestCase

from judgments.templatetags.errors import error_messages


class TestErrorFilters(TestCase):
    def test_error_messages_form_level(self):
        error_message = {"__all__": ["There is an error!"]}
        expected_error_message = "Errors in form - see below for details"

        actual_error_message = error_messages(error_message)

        self.assertEqual(expected_error_message, actual_error_message)

    def test_error_messages_field_level(self):
        error_message = {"form_field": ["There is an error!"]}
        expected_error_message = "Errors in 'form field' - see below for details"

        actual_error_message = error_messages(error_message)

        self.assertEqual(expected_error_message, actual_error_message)

    def test_error_messages_field_level_multi(self):
        error_message = {
            "form_field1": ["There is an error!"],
            "form_field2": ["There is an error!"],
            "form_field3": ["There is an error!"],
        }
        expected_error_message = "Errors in 'form field1', 'form field2', 'form field3' - see below for details"

        actual_error_message = error_messages(error_message)

        self.assertEqual(expected_error_message, actual_error_message)
