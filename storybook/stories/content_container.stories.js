import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Content container",
    render: renderLoadedHtml,
};

const docs = `
  {% call content_container() %}
    Content goes here
  {% endcall %}
`;

export const ContentContainer = createExampleStory(
    "components/content_container.jinja",
    "content_container_examples",
    docs,
);
