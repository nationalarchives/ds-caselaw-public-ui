import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Link",
    render: renderLoadedHtml,
};

const docs = `
    {% call link() %}
      Default link
    {% endcall %}
`;

export const Link = createExampleStory(
    "components/link.jinja",
    "link_examples",
    docs,
);
