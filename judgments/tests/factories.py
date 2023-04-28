from typing import Any
from unittest.mock import Mock

from caselawclient.models.judgments import Judgment


class JudgmentFactory:
    # "name_of_attribute": ("name of incoming param", "default value")
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
    def build(cls, **kwargs) -> Judgment:
        judgment_mock = Mock(spec=Judgment, autospec=True)

        if "html" in kwargs:
            judgment_mock.return_value.content_as_html.return_value = kwargs.pop("html")
        else:
            judgment_mock.return_value.content_as_html.return_value = (
                "<p>This is a judgment.</p>"
            )

        for param, value in cls.PARAMS_MAP.items():
            if param in kwargs:
                setattr(judgment_mock.return_value, param, kwargs[param])
            else:
                setattr(judgment_mock.return_value, param, value)

        return judgment_mock()
