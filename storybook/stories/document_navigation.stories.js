import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Document Navigation Examples",
};

// --------------------
// DocumentNavigation  (wrapper macro)
// --------------------
export const DocumentNavigation = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/document_navigation_examples.jinja",
                "default",
                {},
            );
            return { html };
        },
    ],
    render: (args, context) => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML =
            context.loaded?.html || "<div>No HTML returned</div>";
        return wrapper;
    },
};

// DocumentNavigation loader
// --------------------
const DocumentNavigationLoader = (args) =>
    renderComponentHtml(
        "components/document_navigation.jinja",
        "document_navigation",
        args,
    ).then((html) => ({ html }));

// --------------------
// DocumentNavigation render
// --------------------
const DocumentNavigationRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};

// --------------------
// Individual Navigation
// --------------------
export const JudgmentNavigation = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/document_navigation_examples.jinja",
                "judgment_navigation",
                {},
            );
            return { html };
        },
    ],
    render: (args, context) => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML =
            context.loaded?.html || "<div>No HTML returned</div>";
        return wrapper;
    },
};
