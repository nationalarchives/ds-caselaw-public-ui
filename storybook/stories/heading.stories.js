import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Heading",
    render: renderLoadedHtml,
};

const docs = `
  {% call heading() %}
    Content
  {% endcall %}
`;

export const Heading = createExampleStory(
    "components/heading.jinja",
    "heading_examples",
    docs,
);
