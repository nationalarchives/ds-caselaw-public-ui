import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Navigation",
    render: renderLoadedHtml,
};

const docs = `
{{ navigation() }}
`;

export const Navigation = createExampleStory(
    "components/navigation.jinja",
    "navigation",
    docs,
);
