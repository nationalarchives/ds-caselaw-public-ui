import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Grid",
    render: renderLoadedHtml,
};

const docs = `
  {% call grid() %}
    <div>Grid item 1</div>
    <div>Grid item 2</div>
    <div>Grid item 3</div>
  {% endcall %}
`;

export const Grid = createExampleStory(
    "components/grid.jinja",
    "grid_examples",
    docs,
);
