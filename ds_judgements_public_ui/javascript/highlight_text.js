document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get("query");

    if (!query) return;

    const regex = new RegExp(`(${query})`, "gi");

    function highlightText(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const match = node.nodeValue.match(regex);
            if (match) {
                const span = document.createElement("span");
                span.innerHTML = node.nodeValue.replace(
                    regex,
                    "<mark>$1</mark>",
                );
                node.replaceWith(span);
            }
        } else if (
            node.nodeType === Node.ELEMENT_NODE &&
            node.tagName !== "SCRIPT" &&
            node.tagName !== "STYLE" &&
            node.tagName !== "MARK"
        ) {
            for (let child of Array.from(node.childNodes)) {
                highlightText(child);
            }
        }
    }

    const container = document.querySelector("[data-document-body]");
    if (container) {
        highlightText(container);
    }
});
