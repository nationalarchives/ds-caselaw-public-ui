module.exports = {
    extends: [
        "stylelint-config-standard-scss",
        "stylelint-config-clean-order/error",
    ],
    rules: {
        "selector-class-pattern": [
            "^[a-z]([-]?[a-z0-9]+)*(__[a-z0-9]([-]?[a-z0-9]+)*)?(--[a-z0-9]([-]?[a-z0-9]+)*)?$",
            {
                resolveNestedSelectors: true,
                message: function expected(selectorValue) {
                    return `Expected class selector "${selectorValue}" to match BEM CSS pattern.`;
                },
            },
        ],
    },
};
