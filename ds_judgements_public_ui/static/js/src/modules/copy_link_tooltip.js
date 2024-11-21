const copyLinkToClipboard = function (event, textToCopy) {
    event.preventDefault();
    event.stopPropagation();
    navigator.clipboard.writeText(textToCopy);
};

const createTooltipElement = function (text) {
    const element = document.createElement("span");

    element.classList.add("copy-to-clipboard-link__tooltip");
    element.innerHTML = text;

    return element;
};

const addCopyLinkTooltip = function (link) {
    if (!link || !(link instanceof HTMLElement)) return;

    const tooltipText = link.dataset.copyLinkTooltip;

    const tooltip = createTooltipElement(tooltipText);

    link.append(tooltip);

    link.addEventListener("click", function (event) {
        copyLinkToClipboard(event, link.href);
        tooltip.innerHTML = "Copied!";

        setTimeout(() => {
            tooltip.innerHTML = tooltipText;
        }, 3000);
    });
};

const setupCopyLinkTooltips = function () {
    const links = document.querySelectorAll("[data-copy-link-tooltip]");

    links.forEach(function (link) {
        addCopyLinkTooltip(link);
    });
};

document.addEventListener("DOMContentLoaded", setupCopyLinkTooltips);
