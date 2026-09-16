export function showBackToTopLinks() {
    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end",
    );
    const skipToEndLinkContainer = document.getElementById(
        "js-document-navigation-links-start",
    );

    if (!backToTopLinkContainer) return;

    if (skipToEndLinkContainer) {
        skipToEndLinkContainer.classList.add("autohide");

        while (skipToEndLinkContainer.firstChild) {
            backToTopLinkContainer.appendChild(
                skipToEndLinkContainer.firstChild,
            );
        }
    }

    backToTopLinkContainer.classList.add("show");
}

export function updateDocumentNavigationLinkText() {
    const urlParams = new URLSearchParams(window.location.search);
    const hasQuery = urlParams.has("query");

    if (!hasQuery) return;

    const startLink = document.getElementById("start-of-document-link");
    const endLink = document.getElementById("end-of-document-link");

    if (startLink) {
        startLink.textContent = "Top";
    }

    if (endLink) {
        endLink.textContent = "End";
    }
}
