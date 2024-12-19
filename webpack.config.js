const path = require("path");

module.exports = {
    mode: "production",
    devtool: false,
    entry: {
        app: "./ds_judgements_public_ui/static/js/src/app.js",
        manage_filters:
            "./ds_judgements_public_ui/static/js/src/manage_filters.js",
        document_navigation_links:
            "./ds_judgements_public_ui/static/js/src/document_navigation_links.js",
        location_picker:
            "./ds_judgements_public_ui/static/js/src/location_picker.js",
        transactional_licence_form:
            "./ds_judgements_public_ui/static/js/src/transactional_licence_form.js",
        document_paragraph_tooltip_anchors:
            "./ds_judgements_public_ui/static/js/src/document_paragraph_tooltip_anchors.js",
        copy_link_tooltip:
            "./ds_judgements_public_ui/static/js/src/copy_link_tooltip.js",
        cookie_consent:
            "./ds_judgements_public_ui/static/js/cookie_consent/src/ds-cookie-consent.js",
        gtm_script: "./ds_judgements_public_ui/static/js/src/gtm_script.js",
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
