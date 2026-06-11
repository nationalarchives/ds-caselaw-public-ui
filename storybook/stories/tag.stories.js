import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Tag",
    render: renderLoadedHtml,
};

const docs = `
  {% call tag(variant="button") %}
    Button variant
  {% endcall %}
`;

export const Tag = createExampleStory(
    "components/tag.jinja",
    "tag_examples",
    docs,
);
