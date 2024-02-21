import datetime
from typing import Any
from unittest.mock import Mock

from caselawclient.models.documents import Document
from caselawclient.models.judgments import Judgment
from caselawclient.models.press_summaries import PressSummary


class DocumentFactory:
    target_class = Document

    # "name_of_attribute": ("name of incoming param", "default value")
    PARAMS_MAP: dict[str, Any] = {
        "uri": "test/2023/123",
        "name": "Judgment v Judgement",
        "neutral_citation": "[2023] Test 123",
        "court": "Court of Testing",
        "judgment_date_as_string": "2023-02-03",
        "document_date_as_string": "2023-02-03",
        "document_date_as_date": datetime.date.today(),
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
        "document_noun": "document",
    }

    @classmethod
    def build(cls, **kwargs) -> Document:
        judgment_mock = Mock(spec=cls.target_class, autospec=True)

        judgment_mock.return_value.content_as_html.return_value = kwargs.pop(
            "html",
            "<p>This is a judgment in HTML.</p>",
        )

        judgment_mock.return_value.content_as_xml = kwargs.pop(
            "xml",
            """
            <?xml version="1.0" encoding="UTF-8"?>
            <judgment>
                <p>This is a judgment in XML.</p>
            </judgment>
            """,
        )

        for param, value in cls.PARAMS_MAP.items():
            if param in kwargs:
                setattr(judgment_mock.return_value, param, kwargs[param])
            else:
                setattr(judgment_mock.return_value, param, value)

        judgment_mock.return_value.best_human_identifier = kwargs.get(
            "neutral_citation"
        ) or cls.PARAMS_MAP.get("neutral_citation")
        return judgment_mock()


class JudgmentFactory(DocumentFactory):
    target_class = Judgment
    PARAMS_MAP = dict(DocumentFactory.PARAMS_MAP)
    PARAMS_MAP["document_noun"] = "judgment"


class PressSummaryFactory(DocumentFactory):
    target_class = PressSummary
    PARAMS_MAP = dict(DocumentFactory.PARAMS_MAP)
    PARAMS_MAP["document_noun"] = "press summary"
