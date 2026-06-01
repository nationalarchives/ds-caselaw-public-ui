import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Divider",
    render: renderLoadedHtml,
};

const docs = `
    {{ divider() }}
`;

export const Divider = createExampleStory(
    "components/divider.jinja",
    "divider",
    docs,
);
