import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Alert Examples",
};

// --------------------
// All Alerts (wrapper macro)
// --------------------
export const AllAlerts = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/alert_examples.jinja",
                "default_alert",
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
// Alert loader
// --------------------
const AlertLoader = (args) =>
    renderComponentHtml("components/alert.jinja", "alert", args).then(
        (html) => ({ html }),
    );

// --------------------
// Alert render
// --------------------
const Render = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};

// --------------------
// Individual Alerts
// --------------------
export const DefaultAlert = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/alert_examples.jinja",
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

export const SmallAlert = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/alert_examples.jinja",
                "small",
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

export const ErrorAlert = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/alert_examples.jinja",
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

export const SuccessAlert = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/alert_examples.jinja",
                "success",
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
