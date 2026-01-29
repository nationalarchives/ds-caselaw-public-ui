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

    // Proxy /storybook-render to Django
    webpackFinal: async (config) => {
        config.devServer = {
            ...config.devServer,
            proxy: {
                "/storybook-render": {
                    target: "http://localhost:3000",
                    changeOrigin: true,
                },
            },
        };
        return config;
    },
};
