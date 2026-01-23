import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/<Component Name> Examples",
};

// --------------------
// <Component Name> (wrapper macro)
// --------------------
export const ComponentName = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/<component>_examples.jinja",
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
// <Component Name> loader
// --------------------
const ComponentNameLoader = (args) =>
    renderComponentHtml(
        "components/<component>.jinja",
        "<base_macro_name>",
        args,
    ).then((html) => ({ html }));

// --------------------
// <Component Name> render
// --------------------
const ComponentNameRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};
