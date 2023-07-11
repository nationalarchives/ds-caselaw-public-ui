from typing import Any
from unittest.mock import Mock

from caselawclient.models.documents import Document


class DocumentFactory:
    PARAMS_MAP: dict[str, Any] = {
        "uri": "test/2023/123",
        "name": "Judgment v Judgement",
        "neutral_citation": "[2023] Test 123",
        "court": "Court of Testing",
        "judgment_date_as_string": "2023-02-03",
        "is_published": False,
        "is_sensitive": False,
        "is_anonymised": False,
        "has_supplementary_materials": False,
        "is_failure": False,
        "source_name": "Example Uploader",
        "source_email": "uploader@example.com",
        "consignment_reference": "TDR-12345",
        "assigned_to": "",
        "versions": [],
    }

    @classmethod
    def build(cls, **kwargs) -> Document:
        mock_document = Mock(spec=Document, autospec=True)

        mock_document.return_value.content_as_html.return_value = kwargs.pop(
            "html",
            "<p>This is a judgment in HTML.</p>",
        )

        mock_document.return_value.content_as_xml.return_value = kwargs.pop(
            "xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<judgment>
<p>This is a judgment in XML.</p><
/judgment>""",
        )

        for param, value in cls.PARAMS_MAP.items():
            if param in kwargs:
                setattr(mock_document.return_value, param, kwargs[param])
            else:
                setattr(mock_document.return_value, param, value)

        return mock_document()
