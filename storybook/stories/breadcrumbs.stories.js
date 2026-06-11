import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Breadcrumbs",
    render: renderLoadedHtml,
};

const docs = `
{% call breadcrumbs(prefix="You are in", home="home", home_text="Find Case Law") %}
    {% call breadcrumb(url="/components") %}
        Components
    {% endcall %}
    {% call breadcrumb() %}
        Example components
    {% endcall %}
{% endcall %}
`;

export const Breadcrumbs = createExampleStory(
    "components/breadcrumbs.jinja",
    "breadcrumbs_examples",
    docs,
);
