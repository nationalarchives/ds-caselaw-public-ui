export function getQueryFromUrl(param = "query") {
    const params = new URLSearchParams(window.location.search);
    return params.get(param) || "";
}

export function getMarksInDocumentBody() {
    const bodyContainer = document.querySelector("[data-document-body]");
    if (!bodyContainer) return [];
    return Array.from(bodyContainer.querySelectorAll("mark"));
}
