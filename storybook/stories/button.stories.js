import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Button Examples",
};

// --------------------
// All Buttons (wrapper macro)
// --------------------
export const AllButtons = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/button_examples.jinja",
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
// Individual buttons loader
// --------------------
const ButtonLoader = (args) =>
    renderComponentHtml("components/button.jinja", "button", args).then(
        (html) => ({ html }),
    );

// --------------------
// Individual buttons render
// --------------------
const ButtonRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};

// --------------------
// Individual buttons
// --------------------
export const PrimaryButton = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/button_examples.jinja",
                "primary",
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

export const SecondaryButton = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/button_examples.jinja",
                "secondary",
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
