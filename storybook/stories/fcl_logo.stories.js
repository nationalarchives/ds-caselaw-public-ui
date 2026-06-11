import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/FCL Logo",
    render: renderLoadedHtml,
};

const docs = `
{{ fcl_logo() }}
`;

export const FCLLogo = createExampleStory(
    "components/fcl_logo.jinja",
    "fcl_logo",
    docs,
);
