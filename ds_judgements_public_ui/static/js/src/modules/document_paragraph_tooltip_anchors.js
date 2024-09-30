const isMobile = function () {
    return window.innerWidth < 1135;
};

const getTooltipPositionClass = function () {
    if (isMobile()) return "judgment-body__copy-link-tooltip--top";

    return "judgment-body__copy-link-tooltip--left";
};

const createAnchorElement = function (id, content) {
    const element = document.createElement("a");
    const text = document.createTextNode(content);

    element.href = "#" + id;
    element.classList.add("judgment-body__anchor-link");

    element.appendChild(text);

    return element;
};

const copyLinkToClipboard = function (event, textToCopy) {
    event.preventDefault();
    event.stopPropagation();
    navigator.clipboard.writeText(textToCopy);
};

const createCopyElement = function (textToCopy) {
    const element = document.createElement("span");

    const tooltipClass = getTooltipPositionClass();
    element.classList.add("judgment-body__copy-link-tooltip");
    element.classList.add(tooltipClass);
    element.innerHTML = "Copy link to this paragraph";

    element.addEventListener("click", function (event) {
        copyLinkToClipboard(event, textToCopy);
        element.innerHTML = "Copied!";
        element.classList.add("judgment-body__copy-link-tooltip--show");

        setTimeout(() => {
            element.innerHTML = "Copy link to this paragraph";
            element.classList.remove("judgment-body__copy-link-tooltip--show");
        }, 3000);
    });

    return element;
};

const createCopyableAnchorElement = function (id, content) {
    const anchorElement = createAnchorElement(id, content);

    const copyElement = createCopyElement(anchorElement.href);

    if (isMobile()) {
        anchorElement.addEventListener("click", function (event) {
            copyLinkToClipboard(event, anchorElement.href);
            copyElement.innerHTML = "Copied!";
            copyElement.classList.add("judgment-body__copy-link-tooltip--show");

            setTimeout(function () {
                copyElement.innerHTML = "Copy link to paragraph";
                copyElement.classList.remove(
                    "judgment-body__copy-link-tooltip--show",
                );
            }, 3000);
        });
    }

    anchorElement.append(copyElement);

    return anchorElement;
};

const addDocumentParagraphAnchorLinkToSection = function (section) {
    if (!section || !(section instanceof HTMLElement)) return;
    if (!section.hasAttribute("id")) return;

    const sectionId = section.id;

    const numberElement = section.querySelector(".judgment-body__number");

    if (!numberElement) return;

    const numberContent = numberElement.textContent;
    numberElement.dataset.numberContent = numberContent;
    numberElement.innerHTML = "";

    const copyableAnchorElement = createCopyableAnchorElement(
        sectionId,
        numberContent,
    );

    numberElement.appendChild(copyableAnchorElement);
};

const removeDocumentParagraphAnchorLinkFromSection = function (section) {
    if (!section || !(section instanceof HTMLElement)) return;
    if (!section.hasAttribute("id")) return;

    const numberElement = section.querySelector(".judgment-body__number");

    const numberContent = numberElement.dataset.numberContent;

    numberElement.innerHTML = numberContent;
};

const removeDocumentParagraphTooltipAnchors = function () {
    const sections = document.querySelectorAll(".judgment-body__section");

    sections.forEach(function (section) {
        removeDocumentParagraphAnchorLinkFromSection(section);
    });
};

const debounceResetDocumentParagraphTooltipAnchors = function () {
    let timeout;

    return function () {
        const later = function () {
            clearTimeout(timeout);
            removeDocumentParagraphTooltipAnchors();
            setupDocumentParagraphTooltipAnchors();
        };

        clearTimeout(timeout);

        timeout = setTimeout(later, 400);
    };
};

const resetDocumentParagraphTooltipAnchors =
    debounceResetDocumentParagraphTooltipAnchors();

const setupDocumentParagraphTooltipAnchors = function () {
    if (
        !window.waffleFlags ||
        !window.waffleFlags.some(function (flag) {
            return flag.document_paragraph_tooltip_anchors;
        })
    )
        return;

    const sections = document.querySelectorAll(".judgment-body__section");

    sections.forEach(function (section) {
        addDocumentParagraphAnchorLinkToSection(section);
    });

    window.addEventListener("resize", resetDocumentParagraphTooltipAnchors);
};

document.addEventListener(
    "DOMContentLoaded",
    setupDocumentParagraphTooltipAnchors,
);
