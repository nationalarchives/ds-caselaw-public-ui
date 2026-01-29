(self.webpackChunkstorybook = self.webpackChunkstorybook || []).push([
    [399],
    {
        "./render_jinja.js": function (module) {
            var __dirname = "/";
            const { execSync: execSync } = eval("require('child_process')"),
                path = eval("require('path')");
            module.exports = function renderJinja(
                templatePath,
                macroName,
                args = {},
            ) {
                const cmd = `python "${path.resolve(__dirname, "render_jinja_core.py")}" "${templatePath}" "${macroName}" ${Object.entries(
                    args,
                )
                    .map(
                        ([k, v]) =>
                            `${k}=${"string" == typeof v ? `"${v}"` : v}`,
                    )
                    .join(" ")}`;
                try {
                    return execSync(cmd).toString();
                } catch (error) {
                    return (
                        console.error(
                            "Jinja Execution Error:",
                            error.stderr
                                ? error.stderr.toString()
                                : "Unknown Python Error",
                        ),
                        ""
                    );
                }
            };
        },
        "./stories/button.stories.js": function (
            __unused_webpack_module,
            __webpack_exports__,
            __webpack_require__,
        ) {
            "use strict";
            (__webpack_require__.r(__webpack_exports__),
                __webpack_require__.d(__webpack_exports__, {
                    Primary: function () {
                        return Primary;
                    },
                }));
            const renderJinja = __webpack_require__("./render_jinja.js");
            __webpack_exports__.default = { title: "Components/Button" };
            const Primary = ((args) =>
                renderJinja("components/button.jinja", "button", args)).bind(
                {},
            );
            Primary.parameters = {
                ...Primary.parameters,
                docs: {
                    ...Primary.parameters?.docs,
                    source: {
                        originalSource:
                            'args =>\n// The imported function is now used directly\nrenderJinja("components/button.jinja", "button", args)',
                        ...Primary.parameters?.docs?.source,
                    },
                },
            };
        },
    },
]);
