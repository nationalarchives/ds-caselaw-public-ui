import unittest

from transactional_licence_form.templatetags.transactional_licence_utils import (
    default_if_empty,
    format_value_for_review,
    get_country_name,
    get_field_name,
    get_form,
    get_subwidget_for_other_field,
    has_other_field,
    mailto_with_subject_href,
    submit_label_for_step,
)


class TestTransactionalLicenceTemplateTags(unittest.TestCase):
    def test_mailto_with_subject_href(self):
        result = mailto_with_subject_href("licensing@example.com", "Licence enquiry")

        self.assertEqual(result, "mailto:licensing@example.com?subject=Licence enquiry")

    def test_default_if_empty(self):
        self.assertEqual(default_if_empty("Existing value", "Fallback value"), "Existing value")

    def test_submit_label_for_step(self):
        self.assertEqual(submit_label_for_step("review"), "Submit your application")

    def test_has_other_field(self):
        self.assertTrue(has_other_field(2, {1}))

    def test_get_subwidget_for_other_field(self):
        self.assertEqual(get_subwidget_for_other_field(2, {1: "Other field widget"}), "Other field widget")

    def test_get_field_name(self):
        self.assertEqual(get_field_name("contact_email", {"contact_email": "Email address"}), "Email address")

    def test_get_form(self):
        self.assertEqual(get_form("contact", {"contact": "Contact form"}), "Contact form")

    def test_get_country_name(self):
        self.assertEqual(get_country_name("country:GB"), "United Kingdom")

    def test_format_value_for_review(self):
        self.assertEqual(format_value_for_review(["Research", "Training"], "project_purpose"), "Research, Training")
