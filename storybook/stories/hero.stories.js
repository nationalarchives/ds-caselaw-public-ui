import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Hero",
    render: renderLoadedHtml,
};

const docs = `
  {% call hero() %}
    <h1>Hero heading</h1>
    <h2>Hero subheading</h2>
    <p>Extra hero content goes here</p>
  {% endcall %}
`;

export const Hero = createExampleStory(
    "components/hero.jinja",
    "hero_examples",
    docs,
);
