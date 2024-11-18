import unittest
from unittest.mock import patch

from caselawclient.models.documents import DocumentURIString

from judgments.templatetags.document_utils import formatted_document_uri


class TestDocumentUtils(unittest.TestCase):
    @patch("judgments.utils.formatted_document_uri")
    def test_formatted_document_uri(self, mock_formatted_document_uri):
        document_uri = DocumentURIString("foo/bar")
        formatted_document_uri(document_uri, "xml")

        mock_formatted_document_uri.assert_called_with("foo/bar", "xml")
