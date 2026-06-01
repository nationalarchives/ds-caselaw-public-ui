import { createExampleStory, renderLoadedHtml } from "../helpers.js";

const ALERT_TEMPLATE = "components/alert.jinja";

export default {
    title: "Components/Alert",
    render: renderLoadedHtml,
};

const defaultDocs = `
{% call alert(title="Title") %}
    <p>Content</p>
{% endcall %}
`;

export const DefaultAlert = createExampleStory(
    ALERT_TEMPLATE,
    "alert_default_examples",
    defaultDocs,
);

const smallDocs = `
  {% call alert(title="Small size title", size="sm") %}
    <p>Small size content</p>
  {% endcall %}
`;

export const SmallAlert = createExampleStory(
    ALERT_TEMPLATE,
    "alert_size_examples",
    smallDocs,
);

const errorDocs = `
  {% call alert(title="Error variant",variant="error") %}
    <p>Error variant content</p>
  {% endcall %}
`;

export const ErrorAlert = createExampleStory(
    ALERT_TEMPLATE,
    "alert_error_examples",
    errorDocs,
);

const successDocs = `
  {% call alert(title="Success variant",variant="success") %}
    <p>Success variant content</p>
  {% endcall %}
`;

export const SuccessAlert = createExampleStory(
    ALERT_TEMPLATE,
    "alert_success_examples",
    successDocs,
);
