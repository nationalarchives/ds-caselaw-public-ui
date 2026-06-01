import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/OpenJusticeLicenseLogo",
    render: renderLoadedHtml,
};

const docs = `
{{ open_justice_license_logo() }}
`;

export const OpenJusticeLicenseLogo = createExampleStory(
    "components/open_justice_license_logo.jinja",
    "open_justice_license_logo",
    docs,
);
