module.exports = {
    fakeTimers: { enableGlobally: true },
    testEnvironment: "jsdom",
    transform: {
        "^.+\\.js$": "babel-jest",
    },
    testMatch: [
        "<rootDir>/ds_judgements_public_ui/static/js/tests/**/*.test.js",
    ],
};
