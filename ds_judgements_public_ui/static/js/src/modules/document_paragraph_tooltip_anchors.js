const createAnchorElement = function (id, content) {
    const element = document.createElement("a");
    const text = document.createTextNode(content);

    element.href = "#" + id;
    element.classList.add("judgment-body__anchor-link");

    element.appendChild(text);

    return element;
};

const createCopyElement = function (textToCopy) {
    const element = document.createElement("span");

    element.classList.add("judgment-body__copy-link-tooltip");
    element.innerHTML = "Copy link to this paragraph";

    element.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        navigator.clipboard.writeText(textToCopy);
        element.innerHTML = "Copied!";

        setTimeout(() => {
            element.innerHTML = "Copy link to this paragraph";
        }, 3000);
    });

    return element;
};

const createCopyableAnchorElement = function (id, content) {
    const anchorElement = createAnchorElement(id, content);
    const copyElement = createCopyElement(anchorElement.href);

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
    numberElement.innerHTML = "";

    const copyableAnchorElement = createCopyableAnchorElement(
        sectionId,
        numberContent,
    );

    numberElement.appendChild(copyableAnchorElement);
};

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
};

document.addEventListener(
    "DOMContentLoaded",
    setupDocumentParagraphTooltipAnchors,
);
