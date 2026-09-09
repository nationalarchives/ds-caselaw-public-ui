import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import { defineConfig } from "vite";

const projectRoot = process.cwd();

const jsEntries = {
  "js/dist/app": "static/js/src/app.js",
  "js/dist/document_navigation": "static/js/src/document_navigation.js",
  "js/dist/document_search_links": "static/js/src/document_search_links.js",
  "js/dist/document_paragraph_tooltip_anchors":
    "static/js/src/document_paragraph_tooltip_anchors.js",
  "js/dist/feedback_link": "static/js/src/feedback_link.js",
  "js/dist/gtm_script": "static/js/src/gtm_script.js",
  "js/dist/highlight_text": "static/js/src/highlight_text.js",
  "js/dist/location_picker": "static/js/src/location_picker.js",
  "js/dist/manage_filters": "static/js/src/manage_filters.js",
  "js/dist/transactional_licence_form":
    "static/js/src/transactional_licence_form.js",
  "js/dist/stateful_details": "static/js/src/stateful_details.js",
};

const cssEntries = {
  main: "sass/main.scss",
  document_pdf: "sass/document_pdf.scss",
};

function djangoReloadPlugin() {
  return {
    name: "django-reload",
    configureServer(server) {
      server.watcher.add([
        resolve(projectRoot, "ds_judgements_public_ui/templates/**/*.jinja"),
        resolve(projectRoot, "transactional_licence_form/templates/**/*.jinja"),
        resolve(projectRoot, "judgments/**/*.py"),
        resolve(projectRoot, "config/**/*.py"),
        resolve(projectRoot, "transactional_licence_form/**/*.py"),
      ]);

      server.watcher.on("change", (file) => {
        if (/\.(jinja|py)$/.test(file)) {
          server.ws.send({ type: "full-reload", path: "*" });
        }
      });
    },
  };
}

function assetFileName(assetInfo) {
  const sourceName =
    assetInfo.originalFileNames?.[0] || assetInfo.names?.[0] || "";

  if (sourceName.endsWith("main.scss") || assetInfo.name === "main.css") {
    return "css/main.css";
  }

  if (
    sourceName.endsWith("document_pdf.scss") ||
    assetInfo.name === "document_pdf.css"
  ) {
    return "css/document_pdf.css";
  }

  return "assets/[name][extname]";
}

export default defineConfig(({ command }) => ({
  root: "ds_judgements_public_ui",
  base: command === "serve" ? "/" : "/static/",
  publicDir: false,
  plugins: [djangoReloadPlugin()],
  resolve: {
    // Share the configured colour palette with the case law frontend's Sass.
    dedupe: ["@nationalarchives/frontend"],
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    cors: true,
    origin: "http://localhost:5173",
  },
  css: {
    preprocessorOptions: {
      scss: {
        loadPaths: [resolve(projectRoot, "node_modules")],
        quietDeps: true,
        importers: [
          {
            // Let Sass select GOV.UK's .import.scss compatibility files.
            findFileUrl(url) {
              if (!url.startsWith("govuk-frontend/")) {
                return null;
              }
              return pathToFileURL(resolve(projectRoot, "node_modules", url));
            },
          },
        ],
      },
    },
  },
  build: {
    outDir: "static",
    emptyOutDir: false,
    manifest: "manifest.json",
    sourcemap: false,
    cssCodeSplit: true,
    rollupOptions: {
      input: {
        ...jsEntries,
        ...cssEntries,
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "js/dist/[name].js",
        assetFileNames: assetFileName,
      },
    },
  },
}));
