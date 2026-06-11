import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Banner",
    render: renderLoadedHtml,
};

const docs = `
{% call banner() %}
    <h2>Help us improve this service</h2>
    {% call button(variant="secondary") %}
      Take a short survey
    {% endcall %}
{% endcall %}
`;

export const DefaultBanner = createExampleStory(
    "components/banner.jinja",
    "banner_examples",
    docs,
);
