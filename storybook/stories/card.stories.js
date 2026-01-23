import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Card Examples",
};

// --------------------
// All Cards (wrapper macro)
// --------------------
export const AllCards = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/card_examples.jinja",
                "default_card",
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
// Card loader
// --------------------
const AlertLoader = (args) =>
    renderComponentHtml("components/card.jinja", "card", args).then((html) => ({
        html,
    }));

// --------------------
// Card render
// --------------------
const Render = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};

// --------------------
// Individual Cards
// --------------------
export const DefaultCard = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/card_examples.jinja",
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

export const LightCard = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/card_examples.jinja",
                "light",
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

export const ImageCard = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/card_examples.jinja",
                "image",
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

export const GhostCard = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/card_examples.jinja",
                "ghost",
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
