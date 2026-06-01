import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/DocumentNavigation",
    render: renderLoadedHtml,
};

const docs = `
{% call document_navigation(query="Query", number_of_mentions=42, page_title="Page title") %}
    Test content
{% endcall %}
`;

export const DocumentNavigation = createExampleStory(
    "components/document_navigation.jinja",
    "document_navigation_examples",
    docs,
);
