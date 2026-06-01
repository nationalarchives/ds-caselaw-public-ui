import { createExampleStory, renderLoadedHtml } from "../helpers.js";

const CARD_TEMPLATE = "components/card.jinja";

export default {
    title: "Components/Card",
    render: renderLoadedHtml,
};

const defaultDocs = `
  {% call card(title="Default") %}
    <p>This is the default card style</p>
  {% endcall %}
`;

export const DefaultCard = createExampleStory(
    CARD_TEMPLATE,
    "card_default_examples",
    defaultDocs,
);

const withLinkDocs = `
  {% call card(title="Default - with link", url=url("components")) %}
    <p>This is a default card with a link</p>
  {% endcall %}
`;

export const WithLinkCard = createExampleStory(
    CARD_TEMPLATE,
    "card_with_link_examples",
    withLinkDocs,
);

const lightDocs = `
{% call card(title="Light", variant="light") %}
    <p>This is the light card style</p>
{% endcall %}

{% call card(variant="light") %}
    <button class="button-primary">Button</button>
    <p>Just a light example with a button</p>
{% endcall %}
`;

export const LightCard = createExampleStory(
    CARD_TEMPLATE,
    "card_light_examples",
    lightDocs,
);

const imageDocs = `
  {% call card(title="Image", variant="image", image_url=static("images/modern-magnifying-glass.jpg")) %}
    <p>This is the image card style</p>
  {% endcall %}
`;

export const ImageCard = createExampleStory(
    CARD_TEMPLATE,
    "card_image_examples",
    imageDocs,
);

const ghostDocs = `
  {% call card(title="Ghost", variant="ghost") %}
    <p>This is the ghost card style</p>
  {% endcall %}
`;

export const GhostCard = createExampleStory(
    CARD_TEMPLATE,
    "card_ghost_examples",
    ghostDocs,
);

const ghostWithLinkDocs = `
  {% call card(title="Ghost - with link", variant="ghost", url=url("components")) %}
    <p>This is a ghost card with a link</p>
  {% endcall %}
`;

export const GhostWithLinkCard = createExampleStory(
    CARD_TEMPLATE,
    "card_ghost_with_link_examples",
    ghostWithLinkDocs,
);
