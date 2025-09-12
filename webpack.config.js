const path = require("path");

module.exports = {
    mode: "production",
    devtool: false,
    entry: {
        app: "./ds_judgements_public_ui/static/js/src/app.js",
        cookie_consent:
            "./ds_judgements_public_ui/static/js/cookie_consent/src/ds-cookie-consent.js",
        document_navigation_links:
            "./ds_judgements_public_ui/static/js/src/document_navigation_links.js",
        document_paragraph_tooltip_anchors:
            "./ds_judgements_public_ui/static/js/src/document_paragraph_tooltip_anchors.js",
        feedback_link:
            "./ds_judgements_public_ui/static/js/src/feedback_link.js",
        govuk_tabs_extended:
            "./ds_judgements_public_ui/static/js/src/govuk_tabs_extended.js",
        gtm_script: "./ds_judgements_public_ui/static/js/src/gtm_script.js",
        location_picker:
            "./ds_judgements_public_ui/static/js/src/location_picker.js",
        manage_filters:
            "./ds_judgements_public_ui/static/js/src/manage_filters.js",
        transactional_licence_form:
            "./ds_judgements_public_ui/static/js/src/transactional_licence_form.js",
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
