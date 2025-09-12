export const setupFeedbackLink = function () {
    const link = document.querySelector("[data-feedback-link]");

    if (!link) return;

    const url = new URL(link.getAttribute("href"), document.baseURI);

    const width = window.innerWidth || document.documentElement.clientWidth;
    const height = window.innerHeight || document.documentElement.clientHeight;

    url.searchParams.set("browser-width", String(width));
    url.searchParams.set("browser-height", String(height));

    link.href = url.toString();
};

document.addEventListener("DOMContentLoaded", setupFeedbackLink);
