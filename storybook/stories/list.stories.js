import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/List",
    render: renderLoadedHtml,
};

const docs = `
  {% call list() %}
    {{ list_item(content="Default list item 1") }}
    {{ list_item(content="Default list item 2") }}
    {{ list_item(content="Default list item 3") }}
  {% endcall %}

  {% call list(variant="horizontal") %}
    {{ list_item(content="Horizontal list item 1") }}
    {{ list_item(content="Horizontal list item 2") }}
    {{ list_item(content="Horizontal list item 3") }}
  {% endcall %}

  {% call list(variant="bullets") %}
    {{ list_item(content="Bullets list item 1") }}
    {{ list_item(content="Bullets list item 2") }}
    {{ list_item(content="Bullets list item 3") }}
  {% endcall %}

  {% call list(variant="decimal") %}
    {{ list_item(content="Decimal list item 1") }}
    {{ list_item(content="Decimal list item 2") }}
    {{ list_item(content="Decimal list item 3") }}
  {% endcall %}
`;

export const List = createExampleStory(
    "components/list.jinja",
    "list_examples",
    docs,
);
