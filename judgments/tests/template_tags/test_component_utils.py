from judgments.templatetags.component_utils import component_class_names


def test_component_class_names_combines_truthy_class_names():
    result = component_class_names("component", None, "component--large extra-class", "")

    assert result == "component component--large extra-class"
