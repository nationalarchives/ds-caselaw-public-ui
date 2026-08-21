import unittest
from unittest.mock import Mock, patch

from caselawclient.types import DocumentURIString

from judgments.templatetags.document_utils import formatted_document_uri, get_title_to_display_in_html


class TestDocumentUtils(unittest.TestCase):
    def test_get_title_to_display_in_html(self):
        document = Mock()
        document.document_noun = "judgment"
        document.body.name = "Example judgment"

        self.assertEqual(get_title_to_display_in_html(document), "Example judgment")

    @patch("judgments.utils.formatted_document_uri")
    def test_formatted_document_uri(self, mock_formatted_document_uri):
        document_uri = DocumentURIString("foo/bar")
        formatted_document_uri(document_uri, "xml")

        mock_formatted_document_uri.assert_called_with("foo/bar", "xml")
