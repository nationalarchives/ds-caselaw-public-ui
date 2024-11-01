module.exports = {
    extends: ["@nationalarchives/ds-caselaw-frontend/stylelint.config.js"],
    ignoreFiles: ["ds_judgements_public_ui/static/css/includes/**/*"],
    rules: {
        "selector-id-pattern": null,
        "no-duplicate-selectors": null,
        "selector-class-pattern": null,
        "scss/at-mixin-pattern": null,
        "no-empty-source": null,
        "number-max-precision": null,
        "no-descending-specificity": null,
        "font-family-no-missing-generic-family-keyword": null,
        "scss/no-global-function-names": null,
        "block-no-empty": null,
        "scss/operator-no-newline-after": null,
        "scss/double-slash-comment-whitespace-inside": null,
        "scss/dollar-variable-pattern": null,
    },
};
