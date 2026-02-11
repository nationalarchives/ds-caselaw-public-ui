import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Breadcrumbs Examples",
};

// --------------------
// Breadcrumbs (wrapper macro)
// --------------------
export const Breadcrumbs = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/breadcrumbs_examples.jinja",
                "default",
                {}, // wrapper macro does not take variant/size
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

// --------------------
// Breadcrumbs loader
// --------------------
const BreadcrumbsLoader = (args) =>
    renderComponentHtml(
        "components/breadcrumbs.jinja",
        "breadcrumb",
        "breadcrumbs",
        args,
    ).then((html) => ({ html }));

// --------------------
// Breadcrumbs render
// --------------------
const BreadcrumbsRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};
