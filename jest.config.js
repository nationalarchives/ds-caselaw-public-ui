module.exports = {
    fakeTimers: { enableGlobally: true },
    testEnvironment: "jsdom",
    transform: {
        "^.+\\.[jt]s$": "babel-jest",
    },
    testMatch: ["<rootDir>/ds_judgements_public_ui/javascript/**/*.test.[jt]s"],
};
