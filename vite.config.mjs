import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import { defineConfig } from "vite";

const projectRoot = process.cwd();

function djangoReloadPlugin() {
  return {
    name: "django-reload",
    configureServer(server) {
      server.watcher.add(
        [
          "ds_judgements_public_ui/templates",
          "transactional_licence_form",
          "judgments",
          "config",
        ].map((directory) => resolve(projectRoot, directory)),
      );

      server.watcher.on("change", (file) => {
        if (/\.(jinja|py)$/.test(file)) {
          server.ws.send({ type: "full-reload", path: "*" });
        }
      });
    },
  };
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
    rollupOptions: {
      input: [
        "static/js/src/app.js",
        "static/js/src/document_navigation.js",
        "static/js/src/document_search_links.js",
        "static/js/src/document_paragraph_tooltip_anchors.js",
        "static/js/src/feedback_link.js",
        "static/js/src/gtm_script.js",
        "static/js/src/highlight_text.js",
        "static/js/src/location_picker.js",
        "static/js/src/manage_filters.js",
        "static/js/src/transactional_licence_form.js",
        "static/js/src/stateful_details.js",
        "sass/main.scss",
        "sass/document_pdf.scss",
      ],
      output: {
        // PDF generation reads css/document_pdf.css directly from disk.
        assetFileNames: (asset) =>
          asset.names.some((name) => name.endsWith(".css"))
            ? "css/[name][extname]"
            : "assets/[name]-[hash][extname]",
      },
    },
  },
}));
