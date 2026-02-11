import renderComponentHtml from "../render_fetch.js";

export default {
    title: "Components/Banner Examples",
};

// --------------------
// Banner (wrapper macro)
// --------------------
export const Banner = {
    loaders: [
        async () => {
            const html = await renderComponentHtml(
                "components/examples/banner_examples.jinja",
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
// Banner loader
// --------------------
const BannerLoader = (args) =>
    renderComponentHtml("components/banner.jinja", "button", args).then(
        (html) => ({ html }),
    );

// --------------------
// Banner render
// --------------------
const BannerRender = (context) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = context.loaded?.html || "<div>No HTML returned</div>";
    return wrapper;
};
