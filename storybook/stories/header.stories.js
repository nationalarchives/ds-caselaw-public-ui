import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Header",
    render: renderLoadedHtml,
};

const docs = `
  {% call header() %}
    Content
  {% endcall %}
`;

export const Header = createExampleStory(
    "components/header.jinja",
    "header_examples",
    docs,
);
