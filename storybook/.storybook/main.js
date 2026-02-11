const STORYBOOK_SERVER =
    process.env.STORYBOOK_SERVER || "http://localhost:3000";

module.exports = {
    stories: ["../stories/**/*.@(mdx|stories.@(js|jsx|ts|tsx))"],

    sidebar: {
        items: ["Introduction"], // Only your Introduction page
    },

    addons: [
        "@storybook/addon-essentials",
        "@storybook/addon-webpack5-compiler-babel",
        "@chromatic-com/storybook",
    ],

    // Use HTML framework
    framework: {
        name: "@storybook/html-webpack5",
        options: {},
    },

    docs: {
        autodocs: false,
    },

    webpackFinal: async (config) => {
        // uses global STORYBOOK_SERVER
        if (
            STORYBOOK_SERVER.includes("localhost") ||
            STORYBOOK_SERVER.includes("0.0.0.0")
        ) {
            config.devServer = {
                ...config.devServer,
                proxy: {
                    "/storybook-render": {
                        target: STORYBOOK_SERVER,
                        changeOrigin: true,
                    },
                    "/static": {
                        target: STORYBOOK_SERVER,
                        changeOrigin: true,
                    },
                },
            };
        }
        return config;
    },
};
