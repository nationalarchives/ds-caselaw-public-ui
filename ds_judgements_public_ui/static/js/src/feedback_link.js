export const setupFeedbackLink = function () {
    const link = document.querySelector("[data-feedback-link]");

    if (!link) return;

    const url = new URL(link.getAttribute("href"), document.baseURI);

    const width = window.innerWidth || document.documentElement.clientWidth;
    const height = window.innerHeight || document.documentElement.clientHeight;

    const uaData = navigator.userAgentData;

    if (uaData && uaData.platform) {
        url.searchParams.set("device-platform", uaData.platform);
        url.searchParams.set(
            "device-class",
            uaData.mobile ? "mobile" : "desktop",
        );
    } else {
        const deviceClass =
            width <= 768 ? "mobile" : width <= 1024 ? "tablet" : "desktop";

        url.searchParams.set("device-class", deviceClass);

        if (navigator.platform) {
            url.searchParams.set("device-platform", navigator.platform);
        }
    }

    url.searchParams.set("browser-width", String(width));
    url.searchParams.set("browser-height", String(height));

    link.href = url.toString();
};

document.addEventListener("DOMContentLoaded", setupFeedbackLink);
