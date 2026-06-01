import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/SearchInput",
    render: renderLoadedHtml,
};

const docs = `
  {% call search_form() %}
      {% call search_form_container() %}
        {{ search_input(label="Search by keyword or neutral citation", button_action=url("advanced_search") , button_label="Search") }}
        {% call search_input_footer() %}
            Footer content goes here
        {% endcall %}
      {% endcall %}
    {% endcall %}
  {% endcall %}
`;

export const SearchInput = createExampleStory(
    "components/search_input.jinja",
    "search_input_examples",
    docs,
);
