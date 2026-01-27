import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";
import cors from "cors";

const app = express();

// Enable CORS for Storybook
app.use(cors());

// Proxy /storybook-render to Django
app.use(
    "/storybook-render",
    createProxyMiddleware({
        target: "http://localhost:3000", // Django server
        changeOrigin: true,
        pathRewrite: { "^/storybook-render": "/storybook-render" },
    }),
);

const PORT = 7000;
app.listen(PORT, () => {
    console.log(`Storybook render proxy running at http://localhost:${PORT}`);
    console.log(`Storybook UI still runs separately at http://localhost:6006`);
});
