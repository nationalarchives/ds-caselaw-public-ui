"""
Custom assertion helpers for tests.
"""

from lxml import html


def parse_html(html_string):
    return html.fromstring(html_string)


def parse_html_fragment_as_fragments(html_string):
    return html.fragments_fromstring(html_string)


def normalise_text(text):
    return " ".join(text.split())


def elements_match(element_1, element_2):
    if element_1.tag != element_2.tag:
        return False

    if (normalise_text(element_1.text or "")) != normalise_text(element_2.text or ""):
        return False

    if element_1.attrib != element_2.attrib:
        return False

    children_1 = list(element_1)
    children_2 = list(element_2)

    if len(children_1) != len(children_2):
        return False

    return all(elements_match(c1, c2) for c1, c2 in zip(children_1, children_2))


def is_contained(container_tree, contained_tree):
    return all(
        any(elements_match(element, fragment) for element in container_tree.iter()) for fragment in contained_tree
    )


def xpath_contents(container_tree, xpath_query):
    elements = container_tree.xpath(xpath_query)

    return [normalise_text(element.text_content()) for element in elements]


def is_contained_by_xpath(container_tree, xpath_query, contained_text):
    normalised_elements = xpath_contents(container_tree, xpath_query)

    return any(normalise_text(contained_text) in normalised_element for normalised_element in normalised_elements)


def response_contains_html(response, contained_html):
    container_tree = parse_html(response.content.decode())
    contained_tree = parse_html_fragment_as_fragments(contained_html)
    return is_contained(container_tree, contained_tree)


def assert_contains_html(response, contained_html):
    assert response_contains_html(response, contained_html)


def assert_not_contains_html(response, contained_html):
    assert not response_contains_html(response, contained_html)


def assert_response_contains_text(response, contained_text, xpath_query):
    container_tree = parse_html(response.content.decode())
    if not is_contained_by_xpath(container_tree, xpath_query, contained_text):
        raise AssertionError(
            f"{contained_text} not found in xpath results {xpath_contents(container_tree, xpath_query)}"
        )


def assert_response_not_contains_text(response, contained_text, xpath_query):
    container_tree = parse_html(response.content.decode())

    assert not is_contained_by_xpath(container_tree, xpath_query, contained_text)
