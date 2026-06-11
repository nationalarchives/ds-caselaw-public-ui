import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Details",
    render: renderLoadedHtml,
};

const docs = `
  {% call details(title="Details") %}
    Contents
  {% endcall %}
`;

export const Contents = createExampleStory(
    "components/details.jinja",
    "details_examples",
    docs,
);
