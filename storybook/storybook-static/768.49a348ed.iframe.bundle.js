"use strict";
(self.webpackChunkstorybook = self.webpackChunkstorybook || []).push([
    [768],
    {
        "./node_modules/@storybook/addon-docs/dist/chunk-H6MOWX77.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                __webpack_require__.d(__webpack_exports__, {
                    VA: function () {
                        return __export;
                    },
                });
                Object.create;
                var __defProp = Object.defineProperty,
                    __export =
                        (Object.getOwnPropertyDescriptor,
                        Object.getOwnPropertyNames,
                        Object.getPrototypeOf,
                        Object.prototype.hasOwnProperty,
                        (target, all) => {
                            for (var name in all)
                                __defProp(target, name, {
                                    get: all[name],
                                    enumerable: !0,
                                });
                        });
            },
        "./node_modules/@storybook/addon-essentials/dist/actions/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        argsEnhancers: function () {
                            return argsEnhancers;
                        },
                        loaders: function () {
                            return loaders;
                        },
                    }));
                var external_STORYBOOK_MODULE_PREVIEW_API_ =
                        __webpack_require__("storybook/internal/preview-api"),
                    external_STORYBOOK_MODULE_CORE_EVENTS_PREVIEW_ERRORS_ =
                        __webpack_require__(
                            "storybook/internal/preview-errors",
                        ),
                    external_STORYBOOK_MODULE_GLOBAL_ =
                        __webpack_require__("@storybook/global");
                var esm_browser_native = {
                    randomUUID:
                        "undefined" != typeof crypto &&
                        crypto.randomUUID &&
                        crypto.randomUUID.bind(crypto),
                };
                let getRandomValues;
                const rnds8 = new Uint8Array(16);
                function rng() {
                    if (
                        !getRandomValues &&
                        ((getRandomValues =
                            "undefined" != typeof crypto &&
                            crypto.getRandomValues &&
                            crypto.getRandomValues.bind(crypto)),
                        !getRandomValues)
                    )
                        throw new Error(
                            "crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported",
                        );
                    return getRandomValues(rnds8);
                }
                const byteToHex = [];
                for (let i = 0; i < 256; ++i)
                    byteToHex.push((i + 256).toString(16).slice(1));
                function unsafeStringify(arr, offset = 0) {
                    return (
                        byteToHex[arr[offset + 0]] +
                        byteToHex[arr[offset + 1]] +
                        byteToHex[arr[offset + 2]] +
                        byteToHex[arr[offset + 3]] +
                        "-" +
                        byteToHex[arr[offset + 4]] +
                        byteToHex[arr[offset + 5]] +
                        "-" +
                        byteToHex[arr[offset + 6]] +
                        byteToHex[arr[offset + 7]] +
                        "-" +
                        byteToHex[arr[offset + 8]] +
                        byteToHex[arr[offset + 9]] +
                        "-" +
                        byteToHex[arr[offset + 10]] +
                        byteToHex[arr[offset + 11]] +
                        byteToHex[arr[offset + 12]] +
                        byteToHex[arr[offset + 13]] +
                        byteToHex[arr[offset + 14]] +
                        byteToHex[arr[offset + 15]]
                    );
                }
                var esm_browser_v4 = function v4(options, buf, offset) {
                        if (esm_browser_native.randomUUID && !buf && !options)
                            return esm_browser_native.randomUUID();
                        const rnds =
                            (options = options || {}).random ||
                            (options.rng || rng)();
                        if (
                            ((rnds[6] = (15 & rnds[6]) | 64),
                            (rnds[8] = (63 & rnds[8]) | 128),
                            buf)
                        ) {
                            offset = offset || 0;
                            for (let i = 0; i < 16; ++i)
                                buf[offset + i] = rnds[i];
                            return buf;
                        }
                        return unsafeStringify(rnds);
                    },
                    config = { depth: 10, clearOnStoryChange: !0, limit: 50 },
                    findProto = (obj, callback) => {
                        let proto = Object.getPrototypeOf(obj);
                        return !proto || callback(proto)
                            ? proto
                            : findProto(proto, callback);
                    },
                    serializeArg = (a) => {
                        if (
                            "object" == typeof (e = a) &&
                            e &&
                            findProto(e, (proto) =>
                                /^Synthetic(?:Base)?Event$/.test(
                                    proto.constructor.name,
                                ),
                            ) &&
                            "function" == typeof e.persist
                        ) {
                            let e = Object.create(
                                a.constructor.prototype,
                                Object.getOwnPropertyDescriptors(a),
                            );
                            e.persist();
                            let viewDescriptor =
                                    Object.getOwnPropertyDescriptor(e, "view"),
                                view = viewDescriptor?.value;
                            return (
                                "object" == typeof view &&
                                    "Window" === view?.constructor.name &&
                                    Object.defineProperty(e, "view", {
                                        ...viewDescriptor,
                                        value: Object.create(
                                            view.constructor.prototype,
                                        ),
                                    }),
                                e
                            );
                        }
                        var e;
                        return a;
                    };
                function action(name, options = {}) {
                    let actionOptions = { ...config, ...options },
                        handler = function (...args) {
                            if (options.implicit) {
                                let storyRenderer = (
                                    "__STORYBOOK_PREVIEW__" in
                                    external_STORYBOOK_MODULE_GLOBAL_.global
                                        ? external_STORYBOOK_MODULE_GLOBAL_
                                              .global.__STORYBOOK_PREVIEW__
                                        : void 0
                                )?.storyRenders.find(
                                    (render) =>
                                        "playing" === render.phase ||
                                        "rendering" === render.phase,
                                );
                                if (storyRenderer) {
                                    let deprecated =
                                            !globalThis?.FEATURES
                                                ?.disallowImplicitActionsInRenderV8,
                                        error =
                                            new external_STORYBOOK_MODULE_CORE_EVENTS_PREVIEW_ERRORS_.ImplicitActionsDuringRendering(
                                                {
                                                    phase: storyRenderer.phase,
                                                    name: name,
                                                    deprecated: deprecated,
                                                },
                                            );
                                    if (!deprecated) throw error;
                                    console.warn(error);
                                }
                            }
                            let channel =
                                    external_STORYBOOK_MODULE_PREVIEW_API_.addons.getChannel(),
                                id =
                                    "object" == typeof crypto &&
                                    "function" == typeof crypto.getRandomValues
                                        ? esm_browser_v4()
                                        : Date.now().toString(36) +
                                          Math.random()
                                              .toString(36)
                                              .substring(2),
                                serializedArgs = args.map(serializeArg),
                                normalizedArgs =
                                    args.length > 1
                                        ? serializedArgs
                                        : serializedArgs[0],
                                actionDisplayToEmit = {
                                    id: id,
                                    count: 0,
                                    data: { name: name, args: normalizedArgs },
                                    options: {
                                        ...actionOptions,
                                        maxDepth:
                                            5 + (actionOptions.depth || 3),
                                        allowFunction:
                                            actionOptions.allowFunction || !1,
                                    },
                                };
                            channel.emit(
                                "storybook/actions/action-event",
                                actionDisplayToEmit,
                            );
                        };
                    return (
                        (handler.isAction = !0),
                        (handler.implicit = options.implicit),
                        handler
                    );
                }
                var isInInitialArgs = (name, initialArgs) =>
                        typeof initialArgs[name] > "u" &&
                        !(name in initialArgs),
                    argsEnhancers = [
                        (context) => {
                            let {
                                initialArgs: initialArgs,
                                argTypes: argTypes,
                                parameters: { actions: actions },
                            } = context;
                            return actions?.disable || !argTypes
                                ? {}
                                : Object.entries(argTypes)
                                      .filter(
                                          ([name, argType]) => !!argType.action,
                                      )
                                      .reduce(
                                          (acc, [name, argType]) => (
                                              isInInitialArgs(
                                                  name,
                                                  initialArgs,
                                              ) &&
                                                  (acc[name] = action(
                                                      "string" ==
                                                          typeof argType.action
                                                          ? argType.action
                                                          : name,
                                                  )),
                                              acc
                                          ),
                                          {},
                                      );
                        },
                        (context) => {
                            let {
                                initialArgs: initialArgs,
                                argTypes: argTypes,
                                id: id,
                                parameters: { actions: actions },
                            } = context;
                            if (
                                !actions ||
                                actions.disable ||
                                !actions.argTypesRegex ||
                                !argTypes
                            )
                                return {};
                            let argTypesRegex = new RegExp(
                                actions.argTypesRegex,
                            );
                            return Object.entries(argTypes)
                                .filter(([name]) => !!argTypesRegex.test(name))
                                .reduce(
                                    (acc, [name, argType]) => (
                                        isInInitialArgs(name, initialArgs) &&
                                            (acc[name] = action(name, {
                                                implicit: !0,
                                                id: id,
                                            })),
                                        acc
                                    ),
                                    {},
                                );
                        },
                    ],
                    subscribed = !1,
                    loaders = [
                        (context) => {
                            let {
                                parameters: { actions: actions },
                            } = context;
                            if (
                                !actions?.disable &&
                                !subscribed &&
                                "__STORYBOOK_TEST_ON_MOCK_CALL__" in
                                    external_STORYBOOK_MODULE_GLOBAL_.global &&
                                "function" ==
                                    typeof external_STORYBOOK_MODULE_GLOBAL_
                                        .global.__STORYBOOK_TEST_ON_MOCK_CALL__
                            ) {
                                ((0,
                                external_STORYBOOK_MODULE_GLOBAL_.global
                                    .__STORYBOOK_TEST_ON_MOCK_CALL__)(
                                    (mock, args) => {
                                        let name = mock.getMockName();
                                        "spy" !== name &&
                                            (!/^next\/.*::/.test(name) ||
                                                [
                                                    "next/router::useRouter()",
                                                    "next/navigation::useRouter()",
                                                    "next/navigation::redirect",
                                                    "next/cache::",
                                                    "next/headers::cookies().set",
                                                    "next/headers::cookies().delete",
                                                    "next/headers::headers().set",
                                                    "next/headers::headers().delete",
                                                ].some((prefix) =>
                                                    name.startsWith(prefix),
                                                )) &&
                                            action(name)(args);
                                    },
                                ),
                                    (subscribed = !0));
                            }
                        },
                    ];
            },
        "./node_modules/@storybook/addon-essentials/dist/backgrounds/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        decorators: function () {
                            return decorators;
                        },
                        initialGlobals: function () {
                            return initialGlobals;
                        },
                        parameters: function () {
                            return parameters;
                        },
                    }));
                var external_STORYBOOK_MODULE_PREVIEW_API_ =
                        __webpack_require__("storybook/internal/preview-api"),
                    external_STORYBOOK_MODULE_GLOBAL_ =
                        __webpack_require__("@storybook/global"),
                    external_STORYBOOK_MODULE_CLIENT_LOGGER_ =
                        __webpack_require__("storybook/internal/client-logger"),
                    esm = __webpack_require__(
                        "./node_modules/ts-dedent/esm/index.js",
                    ),
                    PARAM_KEY = "backgrounds",
                    DEFAULT_BACKGROUNDS = {
                        light: { name: "light", value: "#F8F8F8" },
                        dark: { name: "dark", value: "#333" },
                    },
                    { document: preview_document, window: preview_window } =
                        external_STORYBOOK_MODULE_GLOBAL_.global,
                    isReduceMotionEnabled = () =>
                        !!preview_window?.matchMedia(
                            "(prefers-reduced-motion: reduce)",
                        )?.matches,
                    clearStyles = (selector) => {
                        (Array.isArray(selector)
                            ? selector
                            : [selector]
                        ).forEach(clearStyle);
                    },
                    clearStyle = (selector) => {
                        let element = preview_document.getElementById(selector);
                        element && element.parentElement?.removeChild(element);
                    },
                    addGridStyle = (selector, css) => {
                        let existingStyle =
                            preview_document.getElementById(selector);
                        if (existingStyle)
                            existingStyle.innerHTML !== css &&
                                (existingStyle.innerHTML = css);
                        else {
                            let style = preview_document.createElement("style");
                            (style.setAttribute("id", selector),
                                (style.innerHTML = css),
                                preview_document.head.appendChild(style));
                        }
                    },
                    addBackgroundStyle = (selector, css, storyId) => {
                        let existingStyle =
                            preview_document.getElementById(selector);
                        if (existingStyle)
                            existingStyle.innerHTML !== css &&
                                (existingStyle.innerHTML = css);
                        else {
                            let style = preview_document.createElement("style");
                            (style.setAttribute("id", selector),
                                (style.innerHTML = css));
                            let gridStyleSelector =
                                    "addon-backgrounds-grid" +
                                    (storyId ? `-docs-${storyId}` : ""),
                                existingGridStyle =
                                    preview_document.getElementById(
                                        gridStyleSelector,
                                    );
                            existingGridStyle
                                ? existingGridStyle.parentElement?.insertBefore(
                                      style,
                                      existingGridStyle,
                                  )
                                : preview_document.head.appendChild(style);
                        }
                    },
                    defaultGrid = {
                        cellSize: 100,
                        cellAmount: 10,
                        opacity: 0.8,
                    },
                    transitionStyle = isReduceMotionEnabled()
                        ? ""
                        : "transition: background-color 0.3s;",
                    decorators = globalThis.FEATURES?.backgroundsStoryGlobals
                        ? [
                              (StoryFn, context) => {
                                  let {
                                          globals: globals,
                                          parameters: parameters2,
                                          viewMode: viewMode,
                                          id: id,
                                      } = context,
                                      {
                                          options:
                                              options = DEFAULT_BACKGROUNDS,
                                          disable: disable,
                                          grid: grid = defaultGrid,
                                      } = parameters2[PARAM_KEY] || {},
                                      data = globals[PARAM_KEY] || {},
                                      backgroundName = data.value,
                                      item = backgroundName
                                          ? options[backgroundName]
                                          : void 0,
                                      value = item?.value || "transparent",
                                      showGrid = data.grid || !1,
                                      shownBackground = !!item && !disable,
                                      backgroundSelector =
                                          "docs" === viewMode
                                              ? `#anchor--${id} .docs-story`
                                              : ".sb-show-main",
                                      gridSelector =
                                          "docs" === viewMode
                                              ? `#anchor--${id} .docs-story`
                                              : ".sb-show-main",
                                      isLayoutPadded =
                                          void 0 === parameters2.layout ||
                                          "padded" === parameters2.layout,
                                      defaultOffset =
                                          "docs" === viewMode
                                              ? 20
                                              : isLayoutPadded
                                                ? 16
                                                : 0,
                                      {
                                          cellAmount: cellAmount,
                                          cellSize: cellSize,
                                          opacity: opacity,
                                          offsetX: offsetX = defaultOffset,
                                          offsetY: offsetY = defaultOffset,
                                      } = grid,
                                      backgroundSelectorId =
                                          "docs" === viewMode
                                              ? `addon-backgrounds-docs-${id}`
                                              : "addon-backgrounds-color",
                                      backgroundTarget =
                                          "docs" === viewMode ? id : null;
                                  (0,
                                  external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                      shownBackground
                                          ? addBackgroundStyle(
                                                backgroundSelectorId,
                                                `\n    ${backgroundSelector} {\n      background: ${value} !important;\n      ${transitionStyle}\n      }`,
                                                backgroundTarget,
                                            )
                                          : clearStyles(backgroundSelectorId);
                                  }, [
                                      backgroundSelector,
                                      backgroundSelectorId,
                                      backgroundTarget,
                                      shownBackground,
                                      value,
                                  ]);
                                  let gridSelectorId =
                                      "docs" === viewMode
                                          ? `addon-backgrounds-grid-docs-${id}`
                                          : "addon-backgrounds-grid";
                                  return (
                                      (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                          if (!showGrid)
                                              return void clearStyles(
                                                  gridSelectorId,
                                              );
                                          let gridSize = [
                                              `${cellSize * cellAmount}px ${cellSize * cellAmount}px`,
                                              `${cellSize * cellAmount}px ${cellSize * cellAmount}px`,
                                              `${cellSize}px ${cellSize}px`,
                                              `${cellSize}px ${cellSize}px`,
                                          ].join(", ");
                                          addGridStyle(
                                              gridSelectorId,
                                              `\n        ${gridSelector} {\n          background-size: ${gridSize} !important;\n          background-position: ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px !important;\n          background-blend-mode: difference !important;\n          background-image: linear-gradient(rgba(130, 130, 130, ${opacity}) 1px, transparent 1px),\n           linear-gradient(90deg, rgba(130, 130, 130, ${opacity}) 1px, transparent 1px),\n           linear-gradient(rgba(130, 130, 130, ${opacity / 2}) 1px, transparent 1px),\n           linear-gradient(90deg, rgba(130, 130, 130, ${opacity / 2}) 1px, transparent 1px) !important;\n        }\n      `,
                                          );
                                      }, [
                                          cellAmount,
                                          cellSize,
                                          gridSelector,
                                          gridSelectorId,
                                          showGrid,
                                          offsetX,
                                          offsetY,
                                          opacity,
                                      ]),
                                      StoryFn()
                                  );
                              },
                          ]
                        : [
                              (StoryFn, context) => {
                                  let {
                                          globals: globals,
                                          parameters: parameters2,
                                      } = context,
                                      gridParameters =
                                          parameters2[PARAM_KEY].grid,
                                      isActive =
                                          !0 === globals[PARAM_KEY]?.grid &&
                                          !0 !== gridParameters.disable,
                                      {
                                          cellAmount: cellAmount,
                                          cellSize: cellSize,
                                          opacity: opacity,
                                      } = gridParameters,
                                      isInDocs = "docs" === context.viewMode,
                                      defaultOffset =
                                          void 0 === parameters2.layout ||
                                          "padded" === parameters2.layout
                                              ? 16
                                              : 0,
                                      offsetX =
                                          gridParameters.offsetX ??
                                          (isInDocs ? 20 : defaultOffset),
                                      offsetY =
                                          gridParameters.offsetY ??
                                          (isInDocs ? 20 : defaultOffset),
                                      gridStyles = (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useMemo)(
                                          () =>
                                              `\n      ${"docs" === context.viewMode ? `#anchor--${context.id} .docs-story` : ".sb-show-main"} {\n        background-size: ${[`${cellSize * cellAmount}px ${cellSize * cellAmount}px`, `${cellSize * cellAmount}px ${cellSize * cellAmount}px`, `${cellSize}px ${cellSize}px`, `${cellSize}px ${cellSize}px`].join(", ")} !important;\n        background-position: ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px, ${offsetX}px ${offsetY}px !important;\n        background-blend-mode: difference !important;\n        background-image: linear-gradient(rgba(130, 130, 130, ${opacity}) 1px, transparent 1px),\n         linear-gradient(90deg, rgba(130, 130, 130, ${opacity}) 1px, transparent 1px),\n         linear-gradient(rgba(130, 130, 130, ${opacity / 2}) 1px, transparent 1px),\n         linear-gradient(90deg, rgba(130, 130, 130, ${opacity / 2}) 1px, transparent 1px) !important;\n      }\n    `,
                                          [cellSize],
                                      );
                                  return (
                                      (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                          let selectorId =
                                              "docs" === context.viewMode
                                                  ? `addon-backgrounds-grid-docs-${context.id}`
                                                  : "addon-backgrounds-grid";
                                          isActive
                                              ? addGridStyle(
                                                    selectorId,
                                                    gridStyles,
                                                )
                                              : clearStyles(selectorId);
                                      }, [isActive, gridStyles, context]),
                                      StoryFn()
                                  );
                              },
                              (StoryFn, context) => {
                                  let {
                                          globals: globals,
                                          parameters: parameters2,
                                      } = context,
                                      globalsBackgroundColor =
                                          globals[PARAM_KEY]?.value,
                                      backgroundsConfig =
                                          parameters2[PARAM_KEY],
                                      selectedBackgroundColor = (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useMemo)(
                                          () =>
                                              backgroundsConfig.disable
                                                  ? "transparent"
                                                  : ((
                                                        currentSelectedValue,
                                                        backgrounds = [],
                                                        defaultName,
                                                    ) => {
                                                        if (
                                                            "transparent" ===
                                                            currentSelectedValue
                                                        )
                                                            return "transparent";
                                                        if (
                                                            backgrounds.find(
                                                                (background) =>
                                                                    background.value ===
                                                                    currentSelectedValue,
                                                            ) ||
                                                            currentSelectedValue
                                                        )
                                                            return currentSelectedValue;
                                                        let defaultBackground =
                                                            backgrounds.find(
                                                                (background) =>
                                                                    background.name ===
                                                                    defaultName,
                                                            );
                                                        if (defaultBackground)
                                                            return defaultBackground.value;
                                                        if (defaultName) {
                                                            let availableColors =
                                                                backgrounds
                                                                    .map(
                                                                        (
                                                                            background,
                                                                        ) =>
                                                                            background.name,
                                                                    )
                                                                    .join(", ");
                                                            external_STORYBOOK_MODULE_CLIENT_LOGGER_
                                                                .logger
                                                                .warn(esm.T`
        Backgrounds Addon: could not find the default color "${defaultName}".
        These are the available colors for your story based on your configuration:
        ${availableColors}.
      `);
                                                        }
                                                        return "transparent";
                                                    })(
                                                        globalsBackgroundColor,
                                                        backgroundsConfig.values,
                                                        backgroundsConfig.default,
                                                    ),
                                          [
                                              backgroundsConfig,
                                              globalsBackgroundColor,
                                          ],
                                      ),
                                      isActive = (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useMemo)(
                                          () =>
                                              selectedBackgroundColor &&
                                              "transparent" !==
                                                  selectedBackgroundColor,
                                          [selectedBackgroundColor],
                                      ),
                                      selector =
                                          "docs" === context.viewMode
                                              ? `#anchor--${context.id} .docs-story`
                                              : ".sb-show-main",
                                      backgroundStyles = (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useMemo)(
                                          () =>
                                              `\n      ${selector} {\n        background: ${selectedBackgroundColor} !important;\n        ${isReduceMotionEnabled() ? "" : "transition: background-color 0.3s;"}\n      }\n    `,
                                          [selectedBackgroundColor, selector],
                                      );
                                  return (
                                      (0,
                                      external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                          let selectorId =
                                              "docs" === context.viewMode
                                                  ? `addon-backgrounds-docs-${context.id}`
                                                  : "addon-backgrounds-color";
                                          isActive
                                              ? addBackgroundStyle(
                                                    selectorId,
                                                    backgroundStyles,
                                                    "docs" === context.viewMode
                                                        ? context.id
                                                        : null,
                                                )
                                              : clearStyles(selectorId);
                                      }, [isActive, backgroundStyles, context]),
                                      StoryFn()
                                  );
                              },
                          ],
                    parameters = {
                        [PARAM_KEY]: {
                            grid: { cellSize: 20, opacity: 0.5, cellAmount: 5 },
                            disable: !1,
                            ...(!globalThis.FEATURES
                                ?.backgroundsStoryGlobals && {
                                values: Object.values(DEFAULT_BACKGROUNDS),
                            }),
                        },
                    },
                    modern = { [PARAM_KEY]: { value: void 0, grid: !1 } },
                    initialGlobals = globalThis.FEATURES
                        ?.backgroundsStoryGlobals
                        ? modern
                        : { [PARAM_KEY]: null };
            },
        "./node_modules/@storybook/addon-essentials/dist/docs/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        parameters: function () {
                            return parameters;
                        },
                    }));
                (0,
                __webpack_require__(
                    "./node_modules/@storybook/addon-docs/dist/chunk-H6MOWX77.mjs",
                ).VA)({}, { parameters: () => parameters });
                var excludeTags = Object.entries(
                        globalThis.TAGS_OPTIONS ?? {},
                    ).reduce((acc, entry) => {
                        let [tag, option] = entry;
                        return (
                            option.excludeFromDocsStories && (acc[tag] = !0),
                            acc
                        );
                    }, {}),
                    parameters = {
                        docs: {
                            renderer: async () => {
                                let { DocsRenderer: DocsRenderer } =
                                    await Promise.all([
                                        __webpack_require__.e(826),
                                        __webpack_require__.e(980),
                                    ]).then(
                                        __webpack_require__.bind(
                                            __webpack_require__,
                                            "./node_modules/@storybook/addon-docs/dist/DocsRenderer-CFRXHY34.mjs",
                                        ),
                                    );
                                return new DocsRenderer();
                            },
                            stories: {
                                filter: (story) =>
                                    0 ===
                                        (story.tags || []).filter(
                                            (tag) => excludeTags[tag],
                                        ).length &&
                                    !story.parameters.docs?.disable,
                            },
                        },
                    };
            },
        "./node_modules/@storybook/addon-essentials/dist/highlight/preview.mjs":
            function (
                __unused_webpack_module,
                __unused_webpack___webpack_exports__,
                __webpack_require__,
            ) {
                var external_STORYBOOK_MODULE_CORE_EVENTS_ =
                        __webpack_require__("storybook/internal/core-events"),
                    external_STORYBOOK_MODULE_PREVIEW_API_ =
                        __webpack_require__("storybook/internal/preview-api"),
                    external_STORYBOOK_MODULE_GLOBAL_ =
                        __webpack_require__("@storybook/global"),
                    { document: preview_document } =
                        external_STORYBOOK_MODULE_GLOBAL_.global,
                    channel =
                        external_STORYBOOK_MODULE_PREVIEW_API_.addons.getChannel(),
                    resetHighlight = () => {
                        let sheetToBeRemoved =
                            preview_document.getElementById(
                                "storybookHighlight",
                            );
                        sheetToBeRemoved &&
                            sheetToBeRemoved.parentNode?.removeChild(
                                sheetToBeRemoved,
                            );
                    };
                (channel.on(
                    external_STORYBOOK_MODULE_CORE_EVENTS_.STORY_CHANGED,
                    resetHighlight,
                ),
                    channel.on("storybook/highlight/reset", resetHighlight),
                    channel.on("storybook/highlight/add", (infos) => {
                        resetHighlight();
                        let elements = Array.from(new Set(infos.elements)),
                            sheet = preview_document.createElement("style");
                        (sheet.setAttribute("id", "storybookHighlight"),
                            (sheet.innerHTML = elements
                                .map(
                                    (target) =>
                                        `${target}{\n          ${((color = "#FF4785", style = "dashed") => `\n  outline: 2px ${style} ${color};\n  outline-offset: 2px;\n  box-shadow: 0 0 0 6px rgba(255,255,255,0.6);\n`)(infos.color, infos.style)}\n         }`,
                                )
                                .join(" ")),
                            preview_document.head.appendChild(sheet));
                    }));
            },
        "./node_modules/@storybook/addon-essentials/dist/measure/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        decorators: function () {
                            return decorators;
                        },
                        initialGlobals: function () {
                            return initialGlobals;
                        },
                    }));
                var external_STORYBOOK_MODULE_PREVIEW_API_ =
                        __webpack_require__("storybook/internal/preview-api"),
                    external_STORYBOOK_MODULE_GLOBAL_ =
                        __webpack_require__("@storybook/global"),
                    prefix = "Invariant failed";
                function invariant(condition, message) {
                    if (!condition) throw new Error(prefix);
                }
                var PARAM_KEY = "measureEnabled";
                function getDocumentWidthAndHeight() {
                    let container =
                            external_STORYBOOK_MODULE_GLOBAL_.global.document
                                .documentElement,
                        height = Math.max(
                            container.scrollHeight,
                            container.offsetHeight,
                        );
                    return {
                        width: Math.max(
                            container.scrollWidth,
                            container.offsetWidth,
                        ),
                        height: height,
                    };
                }
                function setCanvasWidthAndHeight(
                    canvas,
                    context,
                    { width: width, height: height },
                ) {
                    ((canvas.style.width = `${width}px`),
                        (canvas.style.height = `${height}px`));
                    let scale =
                        external_STORYBOOK_MODULE_GLOBAL_.global.window
                            .devicePixelRatio;
                    ((canvas.width = Math.floor(width * scale)),
                        (canvas.height = Math.floor(height * scale)),
                        context.scale(scale, scale));
                }
                var state = {};
                function init() {
                    state.canvas ||
                        (state = (function createCanvas() {
                            let canvas =
                                external_STORYBOOK_MODULE_GLOBAL_.global.document.createElement(
                                    "canvas",
                                );
                            canvas.id = "storybook-addon-measure";
                            let context = canvas.getContext("2d");
                            invariant(null != context);
                            let { width: width, height: height } =
                                getDocumentWidthAndHeight();
                            return (
                                setCanvasWidthAndHeight(canvas, context, {
                                    width: width,
                                    height: height,
                                }),
                                (canvas.style.position = "absolute"),
                                (canvas.style.left = "0"),
                                (canvas.style.top = "0"),
                                (canvas.style.zIndex = "2147483647"),
                                (canvas.style.pointerEvents = "none"),
                                external_STORYBOOK_MODULE_GLOBAL_.global.document.body.appendChild(
                                    canvas,
                                ),
                                {
                                    canvas: canvas,
                                    context: context,
                                    width: width,
                                    height: height,
                                }
                            );
                        })());
                }
                function clear() {
                    state.context &&
                        state.context.clearRect(
                            0,
                            0,
                            state.width ?? 0,
                            state.height ?? 0,
                        );
                }
                var colors = {
                    margin: "#f6b26b",
                    border: "#ffe599",
                    padding: "#93c47d",
                    content: "#6fa8dc",
                    text: "#232020",
                };
                function roundedRect(
                    context,
                    { x: x, y: y, w: w, h: h, r: r },
                ) {
                    ((x -= w / 2),
                        (y -= h / 2),
                        w < 2 * r && (r = w / 2),
                        h < 2 * r && (r = h / 2),
                        context.beginPath(),
                        context.moveTo(x + r, y),
                        context.arcTo(x + w, y, x + w, y + h, r),
                        context.arcTo(x + w, y + h, x, y + h, r),
                        context.arcTo(x, y + h, x, y, r),
                        context.arcTo(x, y, x + w, y, r),
                        context.closePath());
                }
                function textWithRect(
                    context,
                    type,
                    { x: x, y: y, w: w, h: h },
                    text,
                ) {
                    return (
                        roundedRect(context, { x: x, y: y, w: w, h: h, r: 3 }),
                        (context.fillStyle = `${colors[type]}dd`),
                        context.fill(),
                        (context.strokeStyle = colors[type]),
                        context.stroke(),
                        (context.fillStyle = colors.text),
                        context.fillText(text, x, y),
                        roundedRect(context, { x: x, y: y, w: w, h: h, r: 3 }),
                        (context.fillStyle = `${colors[type]}dd`),
                        context.fill(),
                        (context.strokeStyle = colors[type]),
                        context.stroke(),
                        (context.fillStyle = colors.text),
                        context.fillText(text, x, y),
                        { x: x, y: y, w: w, h: h }
                    );
                }
                function configureText(context, text) {
                    ((context.font = "600 12px monospace"),
                        (context.textBaseline = "middle"),
                        (context.textAlign = "center"));
                    let metrics = context.measureText(text),
                        actualHeight =
                            metrics.actualBoundingBoxAscent +
                            metrics.actualBoundingBoxDescent;
                    return { w: metrics.width + 12, h: actualHeight + 12 };
                }
                function drawLabel(
                    context,
                    measurements,
                    { type: type, position: position = "center", text: text },
                    prevRect,
                    external = !1,
                ) {
                    let { x: x, y: y } = (function positionCoordinate(
                            position,
                            {
                                padding: padding,
                                border: border,
                                width: width,
                                height: height,
                                top: top,
                                left: left,
                            },
                        ) {
                            let contentWidth =
                                    width -
                                    border.left -
                                    border.right -
                                    padding.left -
                                    padding.right,
                                contentHeight =
                                    height -
                                    padding.top -
                                    padding.bottom -
                                    border.top -
                                    border.bottom,
                                x = left + border.left + padding.left,
                                y = top + border.top + padding.top;
                            return (
                                "top" === position
                                    ? (x += contentWidth / 2)
                                    : "right" === position
                                      ? ((x += contentWidth),
                                        (y += contentHeight / 2))
                                      : "bottom" === position
                                        ? ((x += contentWidth / 2),
                                          (y += contentHeight))
                                        : "left" === position
                                          ? (y += contentHeight / 2)
                                          : "center" === position &&
                                            ((x += contentWidth / 2),
                                            (y += contentHeight / 2)),
                                { x: x, y: y }
                            );
                        })(position, measurements),
                        { offsetX: offsetX, offsetY: offsetY } =
                            (function offset(
                                type,
                                position,
                                {
                                    margin: margin,
                                    border: border,
                                    padding: padding,
                                },
                                labelPaddingSize,
                                external,
                            ) {
                                let shift = (dir) => 0,
                                    offsetX = 0,
                                    offsetY = 0,
                                    locationMultiplier = external ? 1 : 0.5,
                                    labelPaddingShift = external
                                        ? 2 * labelPaddingSize
                                        : 0;
                                return (
                                    "padding" === type
                                        ? (shift = (dir) =>
                                              padding[dir] *
                                                  locationMultiplier +
                                              labelPaddingShift)
                                        : "border" === type
                                          ? (shift = (dir) =>
                                                padding[dir] +
                                                border[dir] *
                                                    locationMultiplier +
                                                labelPaddingShift)
                                          : "margin" === type &&
                                            (shift = (dir) =>
                                                padding[dir] +
                                                border[dir] +
                                                margin[dir] *
                                                    locationMultiplier +
                                                labelPaddingShift),
                                    "top" === position
                                        ? (offsetY = -shift("top"))
                                        : "right" === position
                                          ? (offsetX = shift("right"))
                                          : "bottom" === position
                                            ? (offsetY = shift("bottom"))
                                            : "left" === position &&
                                              (offsetX = -shift("left")),
                                    { offsetX: offsetX, offsetY: offsetY }
                                );
                            })(type, position, measurements, 7, external);
                    ((x += offsetX), (y += offsetY));
                    let { w: w, h: h } = configureText(context, text);
                    if (
                        prevRect &&
                        (function collide(a, b) {
                            return (
                                Math.abs(a.x - b.x) < Math.abs(a.w + b.w) / 2 &&
                                Math.abs(a.y - b.y) < Math.abs(a.h + b.h) / 2
                            );
                        })({ x: x, y: y, w: w, h: h }, prevRect)
                    ) {
                        let adjusted = (function overlapAdjustment(
                            position,
                            currentRect,
                            prevRect,
                        ) {
                            return (
                                "top" === position
                                    ? (currentRect.y =
                                          prevRect.y - prevRect.h - 6)
                                    : "right" === position
                                      ? (currentRect.x =
                                            prevRect.x +
                                            prevRect.w / 2 +
                                            6 +
                                            currentRect.w / 2)
                                      : "bottom" === position
                                        ? (currentRect.y =
                                              prevRect.y + prevRect.h + 6)
                                        : "left" === position &&
                                          (currentRect.x =
                                              prevRect.x -
                                              prevRect.w / 2 -
                                              6 -
                                              currentRect.w / 2),
                                { x: currentRect.x, y: currentRect.y }
                            );
                        })(position, { x: x, y: y, w: w, h: h }, prevRect);
                        ((x = adjusted.x), (y = adjusted.y));
                    }
                    return textWithRect(
                        context,
                        type,
                        { x: x, y: y, w: w, h: h },
                        text,
                    );
                }
                function drawStack(context, measurements, stack, external) {
                    let rects = [];
                    stack.forEach((l, idx) => {
                        let rect =
                            external && "center" === l.position
                                ? (function drawFloatingLabel(
                                      context,
                                      measurements,
                                      { type: type, text: text },
                                  ) {
                                      let {
                                              floatingAlignment:
                                                  floatingAlignment2,
                                              extremities: extremities,
                                          } = measurements,
                                          x = extremities[floatingAlignment2.x],
                                          y = extremities[floatingAlignment2.y],
                                          { w: w, h: h } = configureText(
                                              context,
                                              text,
                                          ),
                                          {
                                              offsetX: offsetX,
                                              offsetY: offsetY,
                                          } = (function floatingOffset(
                                              alignment,
                                              { w: w, h: h },
                                          ) {
                                              let deltaW = 0.5 * w + 6,
                                                  deltaH = 0.5 * h + 6;
                                              return {
                                                  offsetX:
                                                      ("left" === alignment.x
                                                          ? -1
                                                          : 1) * deltaW,
                                                  offsetY:
                                                      ("top" === alignment.y
                                                          ? -1
                                                          : 1) * deltaH,
                                              };
                                          })(floatingAlignment2, {
                                              w: w,
                                              h: h,
                                          });
                                      return (
                                          (x += offsetX),
                                          (y += offsetY),
                                          textWithRect(
                                              context,
                                              type,
                                              { x: x, y: y, w: w, h: h },
                                              text,
                                          )
                                      );
                                  })(context, measurements, l)
                                : drawLabel(
                                      context,
                                      measurements,
                                      l,
                                      rects[idx - 1],
                                      external,
                                  );
                        rects[idx] = rect;
                    });
                }
                var colors2_margin = "#f6b26ba8",
                    colors2_border = "#ffe599a8",
                    colors2_padding = "#93c47d8c",
                    colors2_content = "#6fa8dca8";
                function pxToNumber(px) {
                    return parseInt(px.replace("px", ""), 10);
                }
                function round(value) {
                    return Number.isInteger(value) ? value : value.toFixed(2);
                }
                function filterZeroValues(labels) {
                    return labels.filter((l) => 0 !== l.text && "0" !== l.text);
                }
                function floatingAlignment(extremities) {
                    let windowExtremities_top =
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .scrollY,
                        windowExtremities_bottom =
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .scrollY +
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .innerHeight,
                        windowExtremities_left =
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .scrollX,
                        windowExtremities_right =
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .scrollX +
                            external_STORYBOOK_MODULE_GLOBAL_.global.window
                                .innerWidth,
                        distances_top = Math.abs(
                            windowExtremities_top - extremities.top,
                        ),
                        distances_bottom = Math.abs(
                            windowExtremities_bottom - extremities.bottom,
                        );
                    return {
                        x:
                            Math.abs(
                                windowExtremities_left - extremities.left,
                            ) >
                            Math.abs(
                                windowExtremities_right - extremities.right,
                            )
                                ? "left"
                                : "right",
                        y: distances_top > distances_bottom ? "top" : "bottom",
                    };
                }
                function drawBoxModel(element) {
                    return (context) => {
                        if (element && context) {
                            let measurements = (function measureElement(
                                    element,
                                ) {
                                    let style =
                                            external_STORYBOOK_MODULE_GLOBAL_.global.getComputedStyle(
                                                element,
                                            ),
                                        {
                                            top: top,
                                            left: left,
                                            right: right,
                                            bottom: bottom,
                                            width: width,
                                            height: height,
                                        } = element.getBoundingClientRect(),
                                        {
                                            marginTop: marginTop,
                                            marginBottom: marginBottom,
                                            marginLeft: marginLeft,
                                            marginRight: marginRight,
                                            paddingTop: paddingTop,
                                            paddingBottom: paddingBottom,
                                            paddingLeft: paddingLeft,
                                            paddingRight: paddingRight,
                                            borderBottomWidth:
                                                borderBottomWidth,
                                            borderTopWidth: borderTopWidth,
                                            borderLeftWidth: borderLeftWidth,
                                            borderRightWidth: borderRightWidth,
                                        } = style;
                                    ((top +=
                                        external_STORYBOOK_MODULE_GLOBAL_.global
                                            .window.scrollY),
                                        (left +=
                                            external_STORYBOOK_MODULE_GLOBAL_
                                                .global.window.scrollX),
                                        (bottom +=
                                            external_STORYBOOK_MODULE_GLOBAL_
                                                .global.window.scrollY),
                                        (right +=
                                            external_STORYBOOK_MODULE_GLOBAL_
                                                .global.window.scrollX));
                                    let margin = {
                                            top: pxToNumber(marginTop),
                                            bottom: pxToNumber(marginBottom),
                                            left: pxToNumber(marginLeft),
                                            right: pxToNumber(marginRight),
                                        },
                                        padding = {
                                            top: pxToNumber(paddingTop),
                                            bottom: pxToNumber(paddingBottom),
                                            left: pxToNumber(paddingLeft),
                                            right: pxToNumber(paddingRight),
                                        },
                                        border = {
                                            top: pxToNumber(borderTopWidth),
                                            bottom: pxToNumber(
                                                borderBottomWidth,
                                            ),
                                            left: pxToNumber(borderLeftWidth),
                                            right: pxToNumber(borderRightWidth),
                                        },
                                        extremities = {
                                            top: top - margin.top,
                                            bottom: bottom + margin.bottom,
                                            left: left - margin.left,
                                            right: right + margin.right,
                                        };
                                    return {
                                        margin: margin,
                                        padding: padding,
                                        border: border,
                                        top: top,
                                        left: left,
                                        bottom: bottom,
                                        right: right,
                                        width: width,
                                        height: height,
                                        extremities: extremities,
                                        floatingAlignment:
                                            floatingAlignment(extremities),
                                    };
                                })(element),
                                marginLabels = (function drawMargin(
                                    context,
                                    {
                                        margin: margin,
                                        width: width,
                                        height: height,
                                        top: top,
                                        left: left,
                                        bottom: bottom,
                                        right: right,
                                    },
                                ) {
                                    let marginHeight =
                                        height + margin.bottom + margin.top;
                                    return (
                                        (context.fillStyle = colors2_margin),
                                        context.fillRect(
                                            left,
                                            top - margin.top,
                                            width,
                                            margin.top,
                                        ),
                                        context.fillRect(
                                            right,
                                            top - margin.top,
                                            margin.right,
                                            marginHeight,
                                        ),
                                        context.fillRect(
                                            left,
                                            bottom,
                                            width,
                                            margin.bottom,
                                        ),
                                        context.fillRect(
                                            left - margin.left,
                                            top - margin.top,
                                            margin.left,
                                            marginHeight,
                                        ),
                                        filterZeroValues([
                                            {
                                                type: "margin",
                                                text: round(margin.top),
                                                position: "top",
                                            },
                                            {
                                                type: "margin",
                                                text: round(margin.right),
                                                position: "right",
                                            },
                                            {
                                                type: "margin",
                                                text: round(margin.bottom),
                                                position: "bottom",
                                            },
                                            {
                                                type: "margin",
                                                text: round(margin.left),
                                                position: "left",
                                            },
                                        ])
                                    );
                                })(context, measurements),
                                paddingLabels = (function drawPadding(
                                    context,
                                    {
                                        padding: padding,
                                        border: border,
                                        width: width,
                                        height: height,
                                        top: top,
                                        left: left,
                                        bottom: bottom,
                                        right: right,
                                    },
                                ) {
                                    let paddingWidth =
                                            width - border.left - border.right,
                                        paddingHeight =
                                            height -
                                            padding.top -
                                            padding.bottom -
                                            border.top -
                                            border.bottom;
                                    return (
                                        (context.fillStyle = colors2_padding),
                                        context.fillRect(
                                            left + border.left,
                                            top + border.top,
                                            paddingWidth,
                                            padding.top,
                                        ),
                                        context.fillRect(
                                            right -
                                                padding.right -
                                                border.right,
                                            top + padding.top + border.top,
                                            padding.right,
                                            paddingHeight,
                                        ),
                                        context.fillRect(
                                            left + border.left,
                                            bottom -
                                                padding.bottom -
                                                border.bottom,
                                            paddingWidth,
                                            padding.bottom,
                                        ),
                                        context.fillRect(
                                            left + border.left,
                                            top + padding.top + border.top,
                                            padding.left,
                                            paddingHeight,
                                        ),
                                        filterZeroValues([
                                            {
                                                type: "padding",
                                                text: padding.top,
                                                position: "top",
                                            },
                                            {
                                                type: "padding",
                                                text: padding.right,
                                                position: "right",
                                            },
                                            {
                                                type: "padding",
                                                text: padding.bottom,
                                                position: "bottom",
                                            },
                                            {
                                                type: "padding",
                                                text: padding.left,
                                                position: "left",
                                            },
                                        ])
                                    );
                                })(context, measurements),
                                borderLabels = (function drawBorder(
                                    context,
                                    {
                                        border: border,
                                        width: width,
                                        height: height,
                                        top: top,
                                        left: left,
                                        bottom: bottom,
                                        right: right,
                                    },
                                ) {
                                    let borderHeight =
                                        height - border.top - border.bottom;
                                    return (
                                        (context.fillStyle = colors2_border),
                                        context.fillRect(
                                            left,
                                            top,
                                            width,
                                            border.top,
                                        ),
                                        context.fillRect(
                                            left,
                                            bottom - border.bottom,
                                            width,
                                            border.bottom,
                                        ),
                                        context.fillRect(
                                            left,
                                            top + border.top,
                                            border.left,
                                            borderHeight,
                                        ),
                                        context.fillRect(
                                            right - border.right,
                                            top + border.top,
                                            border.right,
                                            borderHeight,
                                        ),
                                        filterZeroValues([
                                            {
                                                type: "border",
                                                text: border.top,
                                                position: "top",
                                            },
                                            {
                                                type: "border",
                                                text: border.right,
                                                position: "right",
                                            },
                                            {
                                                type: "border",
                                                text: border.bottom,
                                                position: "bottom",
                                            },
                                            {
                                                type: "border",
                                                text: border.left,
                                                position: "left",
                                            },
                                        ])
                                    );
                                })(context, measurements),
                                contentLabels = (function drawContent(
                                    context,
                                    {
                                        padding: padding,
                                        border: border,
                                        width: width,
                                        height: height,
                                        top: top,
                                        left: left,
                                    },
                                ) {
                                    let contentWidth =
                                            width -
                                            border.left -
                                            border.right -
                                            padding.left -
                                            padding.right,
                                        contentHeight =
                                            height -
                                            padding.top -
                                            padding.bottom -
                                            border.top -
                                            border.bottom;
                                    return (
                                        (context.fillStyle = colors2_content),
                                        context.fillRect(
                                            left + border.left + padding.left,
                                            top + border.top + padding.top,
                                            contentWidth,
                                            contentHeight,
                                        ),
                                        [
                                            {
                                                type: "content",
                                                position: "center",
                                                text: `${round(contentWidth)} x ${round(contentHeight)}`,
                                            },
                                        ]
                                    );
                                })(context, measurements);
                            !(function labelStacks(
                                context,
                                measurements,
                                labels,
                                externalLabels,
                            ) {
                                let stacks = labels.reduce(
                                    (acc, l) => (
                                        Object.prototype.hasOwnProperty.call(
                                            acc,
                                            l.position,
                                        ) || (acc[l.position] = []),
                                        acc[l.position]?.push(l),
                                        acc
                                    ),
                                    {},
                                );
                                (stacks.top &&
                                    drawStack(
                                        context,
                                        measurements,
                                        stacks.top,
                                        externalLabels,
                                    ),
                                    stacks.right &&
                                        drawStack(
                                            context,
                                            measurements,
                                            stacks.right,
                                            externalLabels,
                                        ),
                                    stacks.bottom &&
                                        drawStack(
                                            context,
                                            measurements,
                                            stacks.bottom,
                                            externalLabels,
                                        ),
                                    stacks.left &&
                                        drawStack(
                                            context,
                                            measurements,
                                            stacks.left,
                                            externalLabels,
                                        ),
                                    stacks.center &&
                                        drawStack(
                                            context,
                                            measurements,
                                            stacks.center,
                                            externalLabels,
                                        ));
                            })(
                                context,
                                measurements,
                                [
                                    ...contentLabels,
                                    ...paddingLabels,
                                    ...borderLabels,
                                    ...marginLabels,
                                ],
                                measurements.width <= 90 ||
                                    measurements.height <= 30,
                            );
                        }
                    };
                }
                function drawSelectedElement(element) {
                    !(function draw(callback) {
                        (clear(), callback(state.context));
                    })(drawBoxModel(element));
                }
                var nodeAtPointerRef,
                    pointer = { x: 0, y: 0 };
                function findAndDrawElement(x, y) {
                    ((nodeAtPointerRef = ((x, y) => {
                        let element =
                                external_STORYBOOK_MODULE_GLOBAL_.global.document.elementFromPoint(
                                    x,
                                    y,
                                ),
                            crawlShadows = (node) => {
                                if (node && node.shadowRoot) {
                                    let nestedElement =
                                        node.shadowRoot.elementFromPoint(x, y);
                                    return node.isEqualNode(nestedElement)
                                        ? node
                                        : nestedElement.shadowRoot
                                          ? crawlShadows(nestedElement)
                                          : nestedElement;
                                }
                                return node;
                            };
                        return crawlShadows(element) || element;
                    })(x, y)),
                        drawSelectedElement(nodeAtPointerRef));
                }
                var decorators = [
                        (StoryFn, context) => {
                            let { measureEnabled: measureEnabled } =
                                context.globals;
                            return (
                                (0,
                                external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                    let onPointerMove = (event) => {
                                        window.requestAnimationFrame(() => {
                                            (event.stopPropagation(),
                                                (pointer.x = event.clientX),
                                                (pointer.y = event.clientY));
                                        });
                                    };
                                    return (
                                        document.addEventListener(
                                            "pointermove",
                                            onPointerMove,
                                        ),
                                        () => {
                                            document.removeEventListener(
                                                "pointermove",
                                                onPointerMove,
                                            );
                                        }
                                    );
                                }, []),
                                (0,
                                external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                    let onResize = () => {
                                        window.requestAnimationFrame(() => {
                                            !(function rescale() {
                                                (invariant(state.canvas),
                                                    invariant(state.context),
                                                    setCanvasWidthAndHeight(
                                                        state.canvas,
                                                        state.context,
                                                        { width: 0, height: 0 },
                                                    ));
                                                let {
                                                    width: width,
                                                    height: height,
                                                } = getDocumentWidthAndHeight();
                                                (setCanvasWidthAndHeight(
                                                    state.canvas,
                                                    state.context,
                                                    {
                                                        width: width,
                                                        height: height,
                                                    },
                                                ),
                                                    (state.width = width),
                                                    (state.height = height));
                                            })();
                                        });
                                    };
                                    return (
                                        "story" === context.viewMode &&
                                            measureEnabled &&
                                            (document.addEventListener(
                                                "pointerover",
                                                (event) => {
                                                    window.requestAnimationFrame(
                                                        () => {
                                                            (event.stopPropagation(),
                                                                findAndDrawElement(
                                                                    event.clientX,
                                                                    event.clientY,
                                                                ));
                                                        },
                                                    );
                                                },
                                            ),
                                            init(),
                                            window.addEventListener(
                                                "resize",
                                                onResize,
                                            ),
                                            findAndDrawElement(
                                                pointer.x,
                                                pointer.y,
                                            )),
                                        () => {
                                            (window.removeEventListener(
                                                "resize",
                                                onResize,
                                            ),
                                                (function destroy() {
                                                    state.canvas &&
                                                        (clear(),
                                                        state.canvas.parentNode?.removeChild(
                                                            state.canvas,
                                                        ),
                                                        (state = {}));
                                                })());
                                        }
                                    );
                                }, [measureEnabled, context.viewMode]),
                                StoryFn()
                            );
                        },
                    ],
                    initialGlobals = { [PARAM_KEY]: !1 };
            },
        "./node_modules/@storybook/addon-essentials/dist/outline/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        decorators: function () {
                            return decorators;
                        },
                        initialGlobals: function () {
                            return initialGlobals;
                        },
                    }));
                var external_STORYBOOK_MODULE_PREVIEW_API_ =
                        __webpack_require__("storybook/internal/preview-api"),
                    external_STORYBOOK_MODULE_GLOBAL_ =
                        __webpack_require__("@storybook/global"),
                    esm = __webpack_require__(
                        "./node_modules/ts-dedent/esm/index.js",
                    ),
                    PARAM_KEY = "outline",
                    clearStyles = (selector) => {
                        (Array.isArray(selector)
                            ? selector
                            : [selector]
                        ).forEach(clearStyle);
                    },
                    clearStyle = (input) => {
                        let selector =
                                "string" == typeof input
                                    ? input
                                    : input.join(""),
                            element =
                                external_STORYBOOK_MODULE_GLOBAL_.global.document.getElementById(
                                    selector,
                                );
                        element &&
                            element.parentElement &&
                            element.parentElement.removeChild(element);
                    };
                var decorators = [
                        (StoryFn, context) => {
                            let { globals: globals } = context,
                                isActive = [!0, "true"].includes(
                                    globals.outline,
                                ),
                                isInDocs = "docs" === context.viewMode,
                                outlineStyles = (0,
                                external_STORYBOOK_MODULE_PREVIEW_API_.useMemo)(
                                    () =>
                                        (function outlineCSS(selector) {
                                            return esm.T`
    ${selector} body {
      outline: 1px solid #2980b9 !important;
    }

    ${selector} article {
      outline: 1px solid #3498db !important;
    }

    ${selector} nav {
      outline: 1px solid #0088c3 !important;
    }

    ${selector} aside {
      outline: 1px solid #33a0ce !important;
    }

    ${selector} section {
      outline: 1px solid #66b8da !important;
    }

    ${selector} header {
      outline: 1px solid #99cfe7 !important;
    }

    ${selector} footer {
      outline: 1px solid #cce7f3 !important;
    }

    ${selector} h1 {
      outline: 1px solid #162544 !important;
    }

    ${selector} h2 {
      outline: 1px solid #314e6e !important;
    }

    ${selector} h3 {
      outline: 1px solid #3e5e85 !important;
    }

    ${selector} h4 {
      outline: 1px solid #449baf !important;
    }

    ${selector} h5 {
      outline: 1px solid #c7d1cb !important;
    }

    ${selector} h6 {
      outline: 1px solid #4371d0 !important;
    }

    ${selector} main {
      outline: 1px solid #2f4f90 !important;
    }

    ${selector} address {
      outline: 1px solid #1a2c51 !important;
    }

    ${selector} div {
      outline: 1px solid #036cdb !important;
    }

    ${selector} p {
      outline: 1px solid #ac050b !important;
    }

    ${selector} hr {
      outline: 1px solid #ff063f !important;
    }

    ${selector} pre {
      outline: 1px solid #850440 !important;
    }

    ${selector} blockquote {
      outline: 1px solid #f1b8e7 !important;
    }

    ${selector} ol {
      outline: 1px solid #ff050c !important;
    }

    ${selector} ul {
      outline: 1px solid #d90416 !important;
    }

    ${selector} li {
      outline: 1px solid #d90416 !important;
    }

    ${selector} dl {
      outline: 1px solid #fd3427 !important;
    }

    ${selector} dt {
      outline: 1px solid #ff0043 !important;
    }

    ${selector} dd {
      outline: 1px solid #e80174 !important;
    }

    ${selector} figure {
      outline: 1px solid #ff00bb !important;
    }

    ${selector} figcaption {
      outline: 1px solid #bf0032 !important;
    }

    ${selector} table {
      outline: 1px solid #00cc99 !important;
    }

    ${selector} caption {
      outline: 1px solid #37ffc4 !important;
    }

    ${selector} thead {
      outline: 1px solid #98daca !important;
    }

    ${selector} tbody {
      outline: 1px solid #64a7a0 !important;
    }

    ${selector} tfoot {
      outline: 1px solid #22746b !important;
    }

    ${selector} tr {
      outline: 1px solid #86c0b2 !important;
    }

    ${selector} th {
      outline: 1px solid #a1e7d6 !important;
    }

    ${selector} td {
      outline: 1px solid #3f5a54 !important;
    }

    ${selector} col {
      outline: 1px solid #6c9a8f !important;
    }

    ${selector} colgroup {
      outline: 1px solid #6c9a9d !important;
    }

    ${selector} button {
      outline: 1px solid #da8301 !important;
    }

    ${selector} datalist {
      outline: 1px solid #c06000 !important;
    }

    ${selector} fieldset {
      outline: 1px solid #d95100 !important;
    }

    ${selector} form {
      outline: 1px solid #d23600 !important;
    }

    ${selector} input {
      outline: 1px solid #fca600 !important;
    }

    ${selector} keygen {
      outline: 1px solid #b31e00 !important;
    }

    ${selector} label {
      outline: 1px solid #ee8900 !important;
    }

    ${selector} legend {
      outline: 1px solid #de6d00 !important;
    }

    ${selector} meter {
      outline: 1px solid #e8630c !important;
    }

    ${selector} optgroup {
      outline: 1px solid #b33600 !important;
    }

    ${selector} option {
      outline: 1px solid #ff8a00 !important;
    }

    ${selector} output {
      outline: 1px solid #ff9619 !important;
    }

    ${selector} progress {
      outline: 1px solid #e57c00 !important;
    }

    ${selector} select {
      outline: 1px solid #e26e0f !important;
    }

    ${selector} textarea {
      outline: 1px solid #cc5400 !important;
    }

    ${selector} details {
      outline: 1px solid #33848f !important;
    }

    ${selector} summary {
      outline: 1px solid #60a1a6 !important;
    }

    ${selector} command {
      outline: 1px solid #438da1 !important;
    }

    ${selector} menu {
      outline: 1px solid #449da6 !important;
    }

    ${selector} del {
      outline: 1px solid #bf0000 !important;
    }

    ${selector} ins {
      outline: 1px solid #400000 !important;
    }

    ${selector} img {
      outline: 1px solid #22746b !important;
    }

    ${selector} iframe {
      outline: 1px solid #64a7a0 !important;
    }

    ${selector} embed {
      outline: 1px solid #98daca !important;
    }

    ${selector} object {
      outline: 1px solid #00cc99 !important;
    }

    ${selector} param {
      outline: 1px solid #37ffc4 !important;
    }

    ${selector} video {
      outline: 1px solid #6ee866 !important;
    }

    ${selector} audio {
      outline: 1px solid #027353 !important;
    }

    ${selector} source {
      outline: 1px solid #012426 !important;
    }

    ${selector} canvas {
      outline: 1px solid #a2f570 !important;
    }

    ${selector} track {
      outline: 1px solid #59a600 !important;
    }

    ${selector} map {
      outline: 1px solid #7be500 !important;
    }

    ${selector} area {
      outline: 1px solid #305900 !important;
    }

    ${selector} a {
      outline: 1px solid #ff62ab !important;
    }

    ${selector} em {
      outline: 1px solid #800b41 !important;
    }

    ${selector} strong {
      outline: 1px solid #ff1583 !important;
    }

    ${selector} i {
      outline: 1px solid #803156 !important;
    }

    ${selector} b {
      outline: 1px solid #cc1169 !important;
    }

    ${selector} u {
      outline: 1px solid #ff0430 !important;
    }

    ${selector} s {
      outline: 1px solid #f805e3 !important;
    }

    ${selector} small {
      outline: 1px solid #d107b2 !important;
    }

    ${selector} abbr {
      outline: 1px solid #4a0263 !important;
    }

    ${selector} q {
      outline: 1px solid #240018 !important;
    }

    ${selector} cite {
      outline: 1px solid #64003c !important;
    }

    ${selector} dfn {
      outline: 1px solid #b4005a !important;
    }

    ${selector} sub {
      outline: 1px solid #dba0c8 !important;
    }

    ${selector} sup {
      outline: 1px solid #cc0256 !important;
    }

    ${selector} time {
      outline: 1px solid #d6606d !important;
    }

    ${selector} code {
      outline: 1px solid #e04251 !important;
    }

    ${selector} kbd {
      outline: 1px solid #5e001f !important;
    }

    ${selector} samp {
      outline: 1px solid #9c0033 !important;
    }

    ${selector} var {
      outline: 1px solid #d90047 !important;
    }

    ${selector} mark {
      outline: 1px solid #ff0053 !important;
    }

    ${selector} bdi {
      outline: 1px solid #bf3668 !important;
    }

    ${selector} bdo {
      outline: 1px solid #6f1400 !important;
    }

    ${selector} ruby {
      outline: 1px solid #ff7b93 !important;
    }

    ${selector} rt {
      outline: 1px solid #ff2f54 !important;
    }

    ${selector} rp {
      outline: 1px solid #803e49 !important;
    }

    ${selector} span {
      outline: 1px solid #cc2643 !important;
    }

    ${selector} br {
      outline: 1px solid #db687d !important;
    }

    ${selector} wbr {
      outline: 1px solid #db175b !important;
    }`;
                                        })(
                                            isInDocs
                                                ? '[data-story-block="true"]'
                                                : ".sb-show-main",
                                        ),
                                    [context],
                                );
                            return (
                                (0,
                                external_STORYBOOK_MODULE_PREVIEW_API_.useEffect)(() => {
                                    let selectorId = isInDocs
                                        ? `addon-outline-docs-${context.id}`
                                        : "addon-outline";
                                    return (
                                        isActive
                                            ? ((selector, css) => {
                                                  let existingStyle =
                                                      external_STORYBOOK_MODULE_GLOBAL_.global.document.getElementById(
                                                          selector,
                                                      );
                                                  if (existingStyle)
                                                      existingStyle.innerHTML !==
                                                          css &&
                                                          (existingStyle.innerHTML =
                                                              css);
                                                  else {
                                                      let style =
                                                          external_STORYBOOK_MODULE_GLOBAL_.global.document.createElement(
                                                              "style",
                                                          );
                                                      (style.setAttribute(
                                                          "id",
                                                          selector,
                                                      ),
                                                          (style.innerHTML =
                                                              css),
                                                          external_STORYBOOK_MODULE_GLOBAL_.global.document.head.appendChild(
                                                              style,
                                                          ));
                                                  }
                                              })(selectorId, outlineStyles)
                                            : clearStyles(selectorId),
                                        () => {
                                            clearStyles(selectorId);
                                        }
                                    );
                                }, [isActive, outlineStyles, context]),
                                StoryFn()
                            );
                        },
                    ],
                    initialGlobals = { [PARAM_KEY]: !1 };
            },
        "./node_modules/@storybook/addon-essentials/dist/viewport/preview.mjs":
            function (
                __unused_webpack_module,
                __webpack_exports__,
                __webpack_require__,
            ) {
                (__webpack_require__.r(__webpack_exports__),
                    __webpack_require__.d(__webpack_exports__, {
                        initialGlobals: function () {
                            return initialGlobals;
                        },
                    }));
                var PARAM_KEY = "viewport",
                    modern = { [PARAM_KEY]: { value: void 0, isRotated: !1 } },
                    initialGlobals = globalThis.FEATURES?.viewportStoryGlobals
                        ? modern
                        : { viewport: "reset", viewportRotated: !1 };
            },
        "./node_modules/@storybook/core/dist/csf/index.js": function (
            __unused_webpack_module,
            __webpack_exports__,
            __webpack_require__,
        ) {
            __webpack_require__.d(__webpack_exports__, {
                aj: function () {
                    return D;
                },
                bU: function () {
                    return W;
                },
                hX: function () {
                    return z;
                },
            });
            var e,
                r,
                _storybook_core_preview_api__WEBPACK_IMPORTED_MODULE_0__ =
                    __webpack_require__("storybook/internal/preview-api"),
                b = Object.create,
                f = Object.defineProperty,
                v = Object.getOwnPropertyDescriptor,
                P = Object.getOwnPropertyNames,
                O = Object.getPrototypeOf,
                _ = Object.prototype.hasOwnProperty,
                s = (e, r) => f(e, "name", { value: r, configurable: !0 }),
                T =
                    ((e = (g) => {
                        (Object.defineProperty(g, "__esModule", { value: !0 }),
                            (g.isEqual = (function () {
                                var e = Object.prototype.toString,
                                    r = Object.getPrototypeOf,
                                    t = Object.getOwnPropertySymbols
                                        ? function (n) {
                                              return Object.keys(n).concat(
                                                  Object.getOwnPropertySymbols(
                                                      n,
                                                  ),
                                              );
                                          }
                                        : Object.keys;
                                return function (n, a) {
                                    return s(function d(o, i, p) {
                                        var c,
                                            u,
                                            l,
                                            m = e.call(o),
                                            h = e.call(i);
                                        if (o === i) return !0;
                                        if (null == o || null == i) return !1;
                                        if (
                                            p.indexOf(o) > -1 &&
                                            p.indexOf(i) > -1
                                        )
                                            return !0;
                                        if (
                                            (p.push(o, i),
                                            m != h ||
                                                ((c = t(o)),
                                                (u = t(i)),
                                                c.length != u.length ||
                                                    c.some(function (A) {
                                                        return !d(
                                                            o[A],
                                                            i[A],
                                                            p,
                                                        );
                                                    })))
                                        )
                                            return !1;
                                        switch (m.slice(8, -1)) {
                                            case "Symbol":
                                                return (
                                                    o.valueOf() == i.valueOf()
                                                );
                                            case "Date":
                                            case "Number":
                                                return (
                                                    +o == +i ||
                                                    (+o != +o && +i != +i)
                                                );
                                            case "RegExp":
                                            case "Function":
                                            case "String":
                                            case "Boolean":
                                                return "" + o == "" + i;
                                            case "Set":
                                            case "Map":
                                                ((c = o.entries()),
                                                    (u = i.entries()));
                                                do {
                                                    if (
                                                        !d(
                                                            (l = c.next())
                                                                .value,
                                                            u.next().value,
                                                            p,
                                                        )
                                                    )
                                                        return !1;
                                                } while (!l.done);
                                                return !0;
                                            case "ArrayBuffer":
                                                ((o = new Uint8Array(o)),
                                                    (i = new Uint8Array(i)));
                                            case "DataView":
                                                ((o = new Uint8Array(o.buffer)),
                                                    (i = new Uint8Array(
                                                        i.buffer,
                                                    )));
                                            case "Float32Array":
                                            case "Float64Array":
                                            case "Int8Array":
                                            case "Int16Array":
                                            case "Int32Array":
                                            case "Uint8Array":
                                            case "Uint16Array":
                                            case "Uint32Array":
                                            case "Uint8ClampedArray":
                                            case "Arguments":
                                            case "Array":
                                                if (o.length != i.length)
                                                    return !1;
                                                for (l = 0; l < o.length; l++)
                                                    if (
                                                        (l in o || l in i) &&
                                                        (l in o != l in i ||
                                                            !d(o[l], i[l], p))
                                                    )
                                                        return !1;
                                                return !0;
                                            case "Object":
                                                return d(r(o), r(i), p);
                                            default:
                                                return !1;
                                        }
                                    }, "n")(n, a, []);
                                };
                            })()));
                    }),
                    () => (
                        r || e((r = { exports: {} }).exports, r),
                        r.exports
                    ));
            function R(e) {
                return e
                    .replace(/_/g, " ")
                    .replace(/-/g, " ")
                    .replace(/\./g, " ")
                    .replace(
                        /([^\n])([A-Z])([a-z])/g,
                        (r, t, n, a) => `${t} ${n}${a}`,
                    )
                    .replace(/([a-z])([A-Z])/g, (r, t, n) => `${t} ${n}`)
                    .replace(/([a-z])([0-9])/gi, (r, t, n) => `${t} ${n}`)
                    .replace(/([0-9])([a-z])/gi, (r, t, n) => `${t} ${n}`)
                    .replace(
                        /(\s|^)(\w)/g,
                        (r, t, n) => `${t}${n.toUpperCase()}`,
                    )
                    .replace(/ +/g, " ")
                    .trim();
            }
            s(R, "toStartCaseStr");
            var y = ((e, r, t) => (
                    (t = null != e ? b(O(e)) : {}),
                    ((e, r, t, n) => {
                        if (
                            (r && "object" == typeof r) ||
                            "function" == typeof r
                        )
                            for (let a of P(r))
                                !_.call(e, a) &&
                                    a !== t &&
                                    f(e, a, {
                                        get: () => r[a],
                                        enumerable:
                                            !(n = v(r, a)) || n.enumerable,
                                    });
                        return e;
                    })(
                        !r && e && e.__esModule
                            ? t
                            : f(t, "default", { value: e, enumerable: !0 }),
                        e,
                    )
                ))(T(), 1),
                x = s(
                    (e) => e.map((r) => typeof r < "u").filter(Boolean).length,
                    "count",
                ),
                E = s((e, r) => {
                    let { exists: t, eq: n, neq: a, truthy: d } = e;
                    if (x([t, n, a, d]) > 1)
                        throw new Error(
                            `Invalid conditional test ${JSON.stringify({ exists: t, eq: n, neq: a })}`,
                        );
                    if (typeof n < "u") return (0, y.isEqual)(r, n);
                    if (typeof a < "u") return !(0, y.isEqual)(r, a);
                    if (typeof t < "u") {
                        let i = typeof r < "u";
                        return t ? i : !i;
                    }
                    return typeof d > "u" || d ? !!r : !r;
                }, "testValue"),
                z = s((e, r, t) => {
                    if (!e.if) return !0;
                    let { arg: n, global: a } = e.if;
                    if (1 !== x([n, a]))
                        throw new Error(
                            `Invalid conditional value ${JSON.stringify({ arg: n, global: a })}`,
                        );
                    let d = n ? r[n] : t[a];
                    return E(e.if, d);
                }, "includeConditionalArg");
            function W(e) {
                return (
                    null != e &&
                    "object" == typeof e &&
                    "_tag" in e &&
                    "Preview" === e?._tag
                );
            }
            function I(e, r) {
                return {
                    _tag: "Meta",
                    input: e,
                    preview: r,
                    get composed() {
                        throw new Error("Not implemented");
                    },
                    story(t) {
                        return U(t, this);
                    },
                };
            }
            function U(e, r) {
                return {
                    _tag: "Story",
                    input: e,
                    meta: r,
                    get composed() {
                        throw new Error("Not implemented");
                    },
                };
            }
            (s(function L(e) {
                let r,
                    t = {
                        _tag: "Preview",
                        input: e,
                        get composed() {
                            if (r) return r;
                            let { addons: n, ...a } = e;
                            return (
                                (r = (0,
                                _storybook_core_preview_api__WEBPACK_IMPORTED_MODULE_0__.normalizeProjectAnnotations)(
                                    (0,
                                    _storybook_core_preview_api__WEBPACK_IMPORTED_MODULE_0__.composeConfigs)(
                                        [...(n ?? []), a],
                                    ),
                                )),
                                r
                            );
                        },
                        meta(n) {
                            return I(n, this);
                        },
                    };
                return ((globalThis.globalProjectAnnotations = t.composed), t);
            }, "__definePreview"),
                s(W, "isPreview"),
                s(function H(e) {
                    return (
                        null != e &&
                        "object" == typeof e &&
                        "_tag" in e &&
                        "Meta" === e?._tag
                    );
                }, "isMeta"),
                s(I, "defineMeta"),
                s(U, "defineStory"),
                s(function K(e) {
                    return (
                        null != e &&
                        "object" == typeof e &&
                        "_tag" in e &&
                        "Story" === e?._tag
                    );
                }, "isStory"));
            var D = s(
                (e) =>
                    e
                        .toLowerCase()
                        .replace(
                            /[ ’–—―′¿'`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi,
                            "-",
                        )
                        .replace(/-+/g, "-")
                        .replace(/^-+/, "")
                        .replace(/-+$/, ""),
                "sanitize",
            );
            function S(e, r) {
                return Array.isArray(r) ? r.includes(e) : e.match(r);
            }
            (s(S, "matches"),
                s(function te(e, { includeStories: r, excludeStories: t }) {
                    return (
                        "__esModule" !== e &&
                        (!r || S(e, r)) &&
                        (!t || !S(e, t))
                    );
                }, "isExportStory"));
        },
        "./node_modules/@storybook/server/dist/entry-preview.mjs": function (
            __unused_webpack_module,
            __webpack_exports__,
            __webpack_require__,
        ) {
            (__webpack_require__.r(__webpack_exports__),
                __webpack_require__.d(__webpack_exports__, {
                    parameters: function () {
                        return parameters;
                    },
                    render: function () {
                        return render;
                    },
                    renderToCanvas: function () {
                        return renderToCanvas;
                    },
                }));
            var storybook_internal_preview_api__WEBPACK_IMPORTED_MODULE_0__ =
                    __webpack_require__("storybook/internal/preview-api"),
                _storybook_global__WEBPACK_IMPORTED_MODULE_1__ =
                    __webpack_require__("@storybook/global"),
                ts_dedent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
                    "./node_modules/ts-dedent/esm/index.js",
                ),
                { fetch: fetch, Node: Node } =
                    _storybook_global__WEBPACK_IMPORTED_MODULE_1__.global,
                defaultFetchStoryHtml = async (
                    url,
                    path,
                    params,
                    storyContext,
                ) => {
                    let fetchUrl = new URL(`${url}/${path}`);
                    return (
                        (fetchUrl.search = new URLSearchParams({
                            ...storyContext.globals,
                            ...params,
                        }).toString()),
                        (await fetch(fetchUrl)).text()
                    );
                },
                buildStoryArgs = (args, argTypes) => {
                    let storyArgs = { ...args };
                    return (
                        Object.keys(argTypes).forEach((key) => {
                            let argType = argTypes[key],
                                { control: control } = argType,
                                controlType =
                                    control &&
                                    "object" == typeof control &&
                                    "type" in control &&
                                    control.type?.toLowerCase(),
                                argValue = storyArgs[key];
                            switch (controlType) {
                                case "date":
                                    storyArgs[key] = new Date(
                                        argValue,
                                    ).toISOString();
                                    break;
                                case "object":
                                    storyArgs[key] = JSON.stringify(argValue);
                            }
                        }),
                        storyArgs
                    );
                },
                render = (args) => {};
            async function renderToCanvas(
                {
                    id: id,
                    title: title,
                    name: name,
                    showMain: showMain,
                    showError: showError,
                    forceRemount: forceRemount,
                    storyFn: storyFn,
                    storyContext: storyContext,
                    storyContext: {
                        parameters: parameters2,
                        args: args,
                        argTypes: argTypes,
                    },
                },
                canvasElement,
            ) {
                storyFn();
                let storyArgs = buildStoryArgs(args, argTypes),
                    {
                        server: {
                            url: url,
                            id: storyId,
                            fetchStoryHtml:
                                fetchStoryHtml = defaultFetchStoryHtml,
                            params: params,
                        },
                    } = parameters2,
                    fetchId = storyId || id,
                    storyParams = { ...params, ...storyArgs },
                    element = await fetchStoryHtml(
                        url,
                        fetchId,
                        storyParams,
                        storyContext,
                    );
                if ((showMain(), "string" == typeof element))
                    ((canvasElement.innerHTML = element),
                        (0,
                        storybook_internal_preview_api__WEBPACK_IMPORTED_MODULE_0__.simulatePageLoad)(
                            canvasElement,
                        ));
                else if (element instanceof Node) {
                    if (
                        canvasElement.firstChild === element &&
                        !1 === forceRemount
                    )
                        return;
                    ((canvasElement.innerHTML = ""),
                        canvasElement.appendChild(element),
                        (0,
                        storybook_internal_preview_api__WEBPACK_IMPORTED_MODULE_0__.simulateDOMContentLoaded)());
                } else
                    showError({
                        title: `Expecting an HTML snippet or DOM node from the story: "${name}" of "${title}".`,
                        description: ts_dedent__WEBPACK_IMPORTED_MODULE_2__.T`
        Did you forget to return the HTML snippet from the story?
        Use "() => <your snippet or node>" or when defining the story.
      `,
                    });
            }
            var parameters = { renderer: "server" };
        },
        "./node_modules/ts-dedent/esm/index.js": function (
            __unused_webpack_module,
            __webpack_exports__,
            __webpack_require__,
        ) {
            function dedent(templ) {
                for (var values = [], _i = 1; _i < arguments.length; _i++)
                    values[_i - 1] = arguments[_i];
                var strings = Array.from(
                    "string" == typeof templ ? [templ] : templ,
                );
                strings[strings.length - 1] = strings[
                    strings.length - 1
                ].replace(/\r?\n([\t ]*)$/, "");
                var indentLengths = strings.reduce(function (arr, str) {
                    var matches = str.match(/\n([\t ]+|(?!\s).)/g);
                    return matches
                        ? arr.concat(
                              matches.map(function (match) {
                                  var _a, _b;
                                  return null !==
                                      (_b =
                                          null ===
                                              (_a = match.match(/[\t ]/g)) ||
                                          void 0 === _a
                                              ? void 0
                                              : _a.length) && void 0 !== _b
                                      ? _b
                                      : 0;
                              }),
                          )
                        : arr;
                }, []);
                if (indentLengths.length) {
                    var pattern_1 = new RegExp(
                        "\n[\t ]{" + Math.min.apply(Math, indentLengths) + "}",
                        "g",
                    );
                    strings = strings.map(function (str) {
                        return str.replace(pattern_1, "\n");
                    });
                }
                strings[0] = strings[0].replace(/^\r?\n/, "");
                var string = strings[0];
                return (
                    values.forEach(function (value, i) {
                        var endentations = string.match(/(?:^|\n)( *)$/),
                            endentation = endentations ? endentations[1] : "",
                            indentedValue = value;
                        ("string" == typeof value &&
                            value.includes("\n") &&
                            (indentedValue = String(value)
                                .split("\n")
                                .map(function (str, i) {
                                    return 0 === i
                                        ? str
                                        : "" + endentation + str;
                                })
                                .join("\n")),
                            (string += indentedValue + strings[i + 1]));
                    }),
                    string
                );
            }
            __webpack_require__.d(__webpack_exports__, {
                T: function () {
                    return dedent;
                },
            });
        },
    },
]);
//# sourceMappingURL=768.49a348ed.iframe.bundle.js.map
