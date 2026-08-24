from judgments.templatetags.text_utils import capfirst, hyphenate


def test_capfirst_capitalises_first_character():
    assert capfirst("judgment") == "Judgment"


def test_hyphenate_returns_slug_like_text():
    assert hyphenate("Open Justice Licence v2") == "open-justice-licence-v2"
