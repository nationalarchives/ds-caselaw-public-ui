import { describe, expect, it, jest } from "@jest/globals";
import {
    updateDocumentNavigationLinkText,
    showBackToTopLinks,
} from "../../src/document_search_links/links";

describe("showBackToTopLinks", () => {
    beforeEach(() => {
        document.body.innerHTML = "";
    });

    it("does nothing if backToTopLinkContainer is missing", () => {
        document.body.innerHTML = `
            <div id="js-document-navigation-links-start">
                <a href="#end">Skip to end</a>
            </div>
        `;

        showBackToTopLinks();

        const skipToEndLinkContainer = document.getElementById(
            "js-document-navigation-links-start",
        );

        expect(skipToEndLinkContainer).not.toBeNull();
        expect(skipToEndLinkContainer.classList.contains("autohide")).toBe(
            false,
        );
    });

    it("adds 'show' class when only backToTopLinkContainer exists", () => {
        document.body.innerHTML = `
            <div id="js-document-navigation-links-end"></div>
        `;

        const backToTopLinkContainer = document.getElementById(
            "js-document-navigation-links-end",
        );

        showBackToTopLinks();

        expect(backToTopLinkContainer).not.toBeNull();
        expect(backToTopLinkContainer.classList.contains("show")).toBe(true);
    });

    it("moves children from skipToEndLinkContainer to backToTopLinkContainer and hides start container", () => {
        document.body.innerHTML = `
            <div id="js-document-navigation-links-start">
                <a id="link-1" href="#one">One</a>
                <a id="link-2" href="#two">Two</a>
            </div>
            <div id="js-document-navigation-links-end"></div>
        `;

        const skipToEndLinkContainer = document.getElementById(
            "js-document-navigation-links-start",
        );
        const backToTopLinkContainer = document.getElementById(
            "js-document-navigation-links-end",
        );

        showBackToTopLinks();

        expect(skipToEndLinkContainer.classList.contains("autohide")).toBe(
            true,
        );
        expect(skipToEndLinkContainer.childNodes.length).toBe(0);

        expect(backToTopLinkContainer.classList.contains("show")).toBe(true);

        const movedLink1 = backToTopLinkContainer.querySelector("#link-1");
        const movedLink2 = backToTopLinkContainer.querySelector("#link-2");

        expect(movedLink1).not.toBeNull();
        expect(movedLink2).not.toBeNull();
        expect(movedLink1.nextElementSibling).toBe(movedLink2);
    });

    it("handles skipToEndLinkContainer with no children gracefully", () => {
        document.body.innerHTML = `
            <div id="js-document-navigation-links-start"></div>
            <div id="js-document-navigation-links-end"></div>
        `;

        const skipToEndLinkContainer = document.getElementById(
            "js-document-navigation-links-start",
        );
        const backToTopLinkContainer = document.getElementById(
            "js-document-navigation-links-end",
        );

        showBackToTopLinks();

        expect(skipToEndLinkContainer.classList.contains("autohide")).toBe(
            true,
        );
        expect(skipToEndLinkContainer.childNodes.length).toBe(0);

        expect(backToTopLinkContainer.classList.contains("show")).toBe(true);
        expect(backToTopLinkContainer.childNodes.length).toBe(0);
    });
});

describe("updateDocumentNavigationLinkText", () => {
    beforeEach(() => {
        document.body.innerHTML = "";
        window.history.pushState({}, "", "/");
    });

    it("does nothing if there is no 'query' parameter", () => {
        document.body.innerHTML = `
            <a id="start-of-document-link">Back to top</a>
            <a id="end-of-document-link">Skip to end</a>
        `;

        updateDocumentNavigationLinkText();

        expect(
            document.getElementById("start-of-document-link").textContent,
        ).toBe("Back to top");
        expect(
            document.getElementById("end-of-document-link").textContent,
        ).toBe("Skip to end");
    });

    it("updates link text if 'query' parameter is present", () => {
        window.history.pushState({}, "", "/?query=test");

        document.body.innerHTML = `
            <a id="start-of-document-link">Back to top</a>
            <a id="end-of-document-link">Skip to end</a>
        `;

        updateDocumentNavigationLinkText();

        expect(
            document.getElementById("start-of-document-link").textContent,
        ).toBe("Top");
        expect(
            document.getElementById("end-of-document-link").textContent,
        ).toBe("End");
    });

    it("only updates existing links when query is present", () => {
        window.history.pushState({}, "", "/?query=1");

        document.body.innerHTML = `<a id="start-of-document-link">Back to top</a>`;

        updateDocumentNavigationLinkText();

        expect(
            document.getElementById("start-of-document-link").textContent,
        ).toBe("Top");
        expect(document.getElementById("end-of-document-link")).toBeNull();
    });

    it("does nothing (and does not throw) if links are missing but query is present", () => {
        window.history.pushState({}, "", "/?query=1");

        updateDocumentNavigationLinkText();

        expect(document.getElementById("start-of-document-link")).toBeNull();
        expect(document.getElementById("end-of-document-link")).toBeNull();
    });
});
