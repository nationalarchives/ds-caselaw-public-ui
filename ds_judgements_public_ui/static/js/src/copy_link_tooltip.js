export const copyLinkToClipboard = function (event, textToCopy) {
    event.preventDefault();
    event.stopPropagation();
    navigator.clipboard.writeText(textToCopy);
};

export const createTooltipElement = function (text) {
    const element = document.createElement("span");

    element.classList.add("copy-to-clipboard-link__tooltip");
    element.innerHTML = text;

    return element;
};

export const addCopyLinkTooltip = function (link) {
    if (!link || !(link instanceof HTMLElement)) return;

    const tooltipText = link.dataset.copyLinkTooltip;

    const tooltip = createTooltipElement(tooltipText);

    link.append(tooltip);

    link.addEventListener("click", function (event) {
        copyLinkToClipboard(event, link.href);
        tooltip.innerHTML = "Copied!";
        tooltip.classList.add("copy-to-clipboard-link__tooltip--copied");

        setTimeout(() => {
            tooltip.innerHTML = tooltipText;
            tooltip.classList.remove("copy-to-clipboard-link__tooltip--copied");
        }, 3000);
    });
};

export const setupCopyLinkTooltips = function () {
    const links = document.querySelectorAll("[data-copy-link-tooltip]");

    links.forEach(function (link) {
        addCopyLinkTooltip(link);
    });
};

document.addEventListener("DOMContentLoaded", setupCopyLinkTooltips);
