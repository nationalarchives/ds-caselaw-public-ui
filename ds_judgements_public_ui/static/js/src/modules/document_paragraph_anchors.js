const setupDocumentParagraphAnchors = function () {
    const sections = document.querySelectorAll(".judgment-body__section");

    sections.forEach(function (section) {
        if (!section.hasAttribute("id")) return;

        const sectionId = section.id;

        const numberElement = section.querySelector(".judgment-body__number");

        if (!numberElement) return;

        const numberContent = numberElement.textContent;

        const anchorElement = document.createElement("a");
        const anchorText = document.createTextNode(numberContent);

        anchorElement.href = "#" + sectionId;

        anchorElement.appendChild(anchorText);

        numberElement.innerHTML = "";
        numberElement.appendChild(anchorElement);
    });
};

document.addEventListener("DOMContentLoaded", setupDocumentParagraphAnchors);
