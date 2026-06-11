import renderComponentHtml from "./render_fetch.js";

const FALLBACK_HTML = "<div>No HTML returned</div>";

export const renderLoadedHtml = (_args, context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || FALLBACK_HTML;
    return wrapper;
};

export const createComponentHtmlLoader =
    (templatePath, componentName, context = {}) =>
    async () => {
        const html = await renderComponentHtml(
            templatePath,
            componentName,
            context,
        );

        return { html };
    };

export const createExampleStory = (templatePath, exampleName, docs = "") => ({
    loaders: [createComponentHtmlLoader(templatePath, exampleName, {})],
    ...{
        parameters: {
            docs: {
                source: {
                    code: docs,
                    language: "django",
                },
            },
        },
    },
});
