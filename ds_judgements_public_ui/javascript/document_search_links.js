import {
    getQueryFromUrl,
    getMarksInDocumentBody,
} from "./document_search_links/utils";
import { createUI } from "./document_search_links/ui";
import { createState } from "./document_search_links/state";
import { attachMarkScrollSync } from "./document_search_links/scrolling";
import {
    showBackToTopLinks,
    updateDocumentNavigationLinkText,
} from "./document_search_links/links";

function initialiseSearchLinks() {
    const marks = getMarksInDocumentBody();
    if (!marks.length) return;

    const linksEndContainer = document.getElementById(
        "js-document-navigation-links-end",
    );
    if (!linksEndContainer) return;

    const queryText = getQueryFromUrl("query");

    const ui = createUI(linksEndContainer, marks.length, queryText);
    if (!ui) return;

    const navState = createState(marks, ui.positionSpan);
    if (!navState) return;

    ui.prevLink.addEventListener("click", (event) => {
        event.preventDefault();
        navState.prev();
    });

    ui.nextLink.addEventListener("click", (event) => {
        event.preventDefault();
        navState.next();
    });

    attachMarkScrollSync(marks, navState);
}

document.addEventListener("DOMContentLoaded", () => {
    showBackToTopLinks();
    updateDocumentNavigationLinkText();
    initialiseSearchLinks();
});
