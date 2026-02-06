module.exports = ({ config }) => {
    // 1. Initialize resolve/alias structures if they don't exist
    if (!config.resolve) {
        config.resolve = {};
    }
    if (!config.resolve.alias) {
        config.resolve.alias = {};
    }

    // 2. CRITICAL: Alias the server modules to 'false' or an empty mock.
    //    This tells the client bundler (Webpack) to ignore these modules,
    //    preventing the 'require is not defined' error.
    config.resolve.alias["child_process"] = false;
    config.resolve.alias["path"] = false; // Include path to prevent related errors

    // 3. Set externals (this is still necessary for the server-side execution context)
    config.externals = ["child_process", "path"];

    return config;
};
