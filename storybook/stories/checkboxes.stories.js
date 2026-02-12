import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Checkboxes Examples",
};

// --------------------
// AllCheckboxes (wrapper macro)
// --------------------
export const AllCheckboxes = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/checkboxes_examples.jinja",
                "default_checkboxes",
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
// Checkboxes loader
// --------------------
const CheckboxesLoader = (args) =>
    renderComponentHtml(
        "components/checkboxes.jinja",
        "govukCheckboxes",
        args,
    ).then((html) => ({ html }));

// --------------------
// Checkboxes render
// --------------------
const CheckboxesRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};

// --------------------
// Individual Checkboxes
// --------------------
export const DefaultCheckbox = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/checkboxes_examples.jinja",
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

export const ErrorCheckbox = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/checkboxes_examples.jinja",
                "error",
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

export const ConditionalCheckbox = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/checkboxes_examples.jinja",
                "conditional",
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
