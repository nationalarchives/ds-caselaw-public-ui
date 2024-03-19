const path = require("path");

module.exports = {
    mode: "production",
    devtool: false,
    entry: {
        app: "./ds_judgements_public_ui/static/js/src/app.js",
        cookie_consent:
            "./ds_judgements_public_ui/static/js/cookie_consent/src/ds-cookie-consent.js",
        gtm_script: "./ds_judgements_public_ui/static/js/src/gtm_script.js",
        "transactional_licence_form/app":
            "./ds_judgements_public_ui/static/js/src/transactional_licence_form/app.js",
    },
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, "ds_judgements_public_ui/static/js/dist"),
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                    },
                },
            },
        ],
    },
};
