const { execSync } = eval("require('child_process')");
const path = eval("require('path')");

/**
Executes the Python script to render the Jinja macro.
 */
module.exports = function renderJinja(templatePath, macroName, args = {}) {
    // Path points to the file you renamed. This is correct.
    const renderScript = path.resolve(__dirname, "render_jinja_core.py");

    // Safely construct argument list, ensuring quotes for shell execution
    const argList = Object.entries(args)
        .map(([k, v]) => {
            // Safely quote arguments, especially important for string inputs.
            const safeValue = typeof v === "string" ? `"${v}"` : v;
            return `${k}=${safeValue}`;
        })
        .join(" ");

    // The command executed: python /path/to/render_jinja_core.py "template/path" "macro" key="value"
    const cmd = `python "${renderScript}" "${templatePath}" "${macroName}" ${argList}`;

    try {
        // Execute the command synchronously and return the output as a string.
        // execSync is available here via the dynamically loaded object.
        return execSync(cmd).toString();
    } catch (error) {
        // Provide a more helpful error message in the storybook iframe
        console.error(
            "Jinja Execution Error:",
            error.stderr ? error.stderr.toString() : "Unknown Python Error",
        );
        return ``;
    }
};
