import { createExampleStory, renderLoadedHtml } from "../helpers.js";

const ICON_TEMPLATE = "components/icon.jinja";

export default {
    title: "Components/Icon",
    render: renderLoadedHtml,
};

const sizeDocs = `
    {{ icon(name="circle_xmark_solid", size="sm") }}
`;

export const Sizes = createExampleStory(
    ICON_TEMPLATE,
    "icon_size_examples",
    sizeDocs,
);

const variantDocs = `
    {{ icon(name="download") }}
`;

export const Variants = createExampleStory(
    ICON_TEMPLATE,
    "icon_variant_examples",
    variantDocs,
);
