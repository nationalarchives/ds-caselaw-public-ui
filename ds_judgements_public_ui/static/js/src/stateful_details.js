const DETAILS_SELECTOR = "[data-stateful-details]";
const CLOSED_TITLE_SELECTOR = "[data-stateful-details-close-title]";
const COOKIE_NAME = "dontShowCookieNotice";
const HIDE_AFTER_MS = 6000;

export function getCookie(name, cookieString = document.cookie) {
    const cookies = cookieString ? cookieString.split("; ") : [];
    for (const c of cookies) {
        const idx = c.indexOf("=");
        const key =
            idx >= 0
                ? decodeURIComponent(c.slice(0, idx))
                : decodeURIComponent(c);

        if (key === name) {
            const val = idx >= 0 ? c.slice(idx + 1) : "";
            return decodeURIComponent(val);
        }
    }
    return null;
}

export function initStatefulDetails(details, options = {}) {
    const {
        closedTitleSelector = CLOSED_TITLE_SELECTOR,
        cookieName = COOKIE_NAME,
        hideAfterMs = HIDE_AFTER_MS,
        cookieString,
    } = options;

    if (!details) return () => {};

    const closedTitle = details.querySelector(closedTitleSelector);
    const summary = details.querySelector("summary");

    const dontShow =
        getCookie(cookieName, cookieString ?? document.cookie) === "true";

    let hideTimerId = null;
    let userHasInteracted = false;

    const showClosedTitle = () => {
        if (!closedTitle) return;

        closedTitle.hidden = false;

        window.clearTimeout(hideTimerId);
        hideTimerId = window.setTimeout(() => {
            closedTitle.hidden = true;
            hideTimerId = null;
        }, hideAfterMs);
    };

    if (closedTitle) closedTitle.hidden = true;

    details.open = !dontShow;

    const onToggle = () => {
        if (!userHasInteracted) return;

        if (details.open) {
            if (closedTitle) closedTitle.hidden = true;
            window.clearTimeout(hideTimerId);
            hideTimerId = null;
        } else {
            if (!dontShow) showClosedTitle();
        }
    };

    const onSummaryClick = () => {
        userHasInteracted = true;
    };

    details.addEventListener("toggle", onToggle);
    if (summary) summary.addEventListener("click", onSummaryClick);

    return () => {
        details.removeEventListener("toggle", onToggle);
        if (summary) summary.removeEventListener("click", onSummaryClick);
        window.clearTimeout(hideTimerId);
        hideTimerId = null;
    };
}

document.addEventListener("DOMContentLoaded", () => {
    const detailsList = Array.from(document.querySelectorAll(DETAILS_SELECTOR));

    return detailsList.map((details) => initStatefulDetails(details, {}));
});
