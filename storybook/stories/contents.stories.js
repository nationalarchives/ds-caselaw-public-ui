import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Contents",
    render: renderLoadedHtml,
};

const docs = `
  {% call contents(title="On this page") %}
    <ul>
      <li>
        <a href="#section-what">What Find Case Law does</a>
      </li>
      <li>
        <a href="#section-pages">Pages in this section</a>
      </li>
    </ul>
  {% endcall %}
`;

export const Contents = createExampleStory(
    "components/contents.jinja",
    "contents_examples",
    docs,
);
