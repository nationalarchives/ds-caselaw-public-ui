import { createExampleStory, renderLoadedHtml } from "../helpers.js";

const BUTTON_TEMPLATE = "components/button.jinja";

export default {
    title: "Components/Button",
    render: renderLoadedHtml,
};

const variantDocs = `
{% call button() %}
    Primary button
{% endcall %}

{% call button(variant="secondary") %}
    Secondary button
{% endcall %}

{% call button(variant="underline") %}
    Underline button
{% endcall %}

{% call button(variant="link") %}
    Link button
{% endcall %}
`;

export const Variants = createExampleStory(
    BUTTON_TEMPLATE,
    "button_variant_examples",
    variantDocs,
);

const sizesDocs = `
{% call button(size="small") %}
    Small primary button
{% endcall %}

{% call button(variant="secondary", size="small") %}
    Small secondary button
{% endcall %}

{% call button(variant="underline", size="small") %}
    Small underline button
{% endcall %}

{% call button(variant="link", size="small") %}
    Small link button
{% endcall %}
`;

export const Sizes = createExampleStory(
    BUTTON_TEMPLATE,
    "button_size_examples",
    sizesDocs,
);

const contrastDocs = `
{% call button(contrast=True) %}
    Primary button
{% endcall %}

{% call button(variant="secondary", contrast=True) %}
    Secondary button
{% endcall %}

{% call button(variant="underline", contrast=True) %}
    Underline button
{% endcall %}
`;

export const Contrast = createExampleStory(
    BUTTON_TEMPLATE,
    "button_contrast_examples",
    contrastDocs,
);

const hrefDocs = `
{% call button(href=url("components")) %}
    Primary
{% endcall %}
`;

export const Href = createExampleStory(
    BUTTON_TEMPLATE,
    "button_href_examples",
    hrefDocs,
);
