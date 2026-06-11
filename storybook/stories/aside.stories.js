import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Aside",
    render: renderLoadedHtml,
};

const docs = `
  {% call aside_container() %}
    <div>Content</div>
    {% call aside() %}
      Aside
    {% endcall %}
  {% endcall %}
`;

export const Aside = createExampleStory(
    "components/aside.jinja",
    "aside_examples",
    docs,
);
