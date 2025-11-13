import { describe, expect, it, beforeEach } from "@jest/globals";
import { createUI } from "../../src/document_search_links/ui";

describe("createUI", () => {
    let linksEndContainer;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="js-document-navigation-links-end"></div>
        `;
        linksEndContainer = document.getElementById(
            "js-document-navigation-links-end",
        );
    });

    it("returns null if linksEndContainer is not provided", () => {
        const ui = createUI(null, 5, "example");
        expect(ui).toBeNull();
    });

    it("adds 'with-query' class when queryText is provided", () => {
        createUI(linksEndContainer, 5, "example");

        expect(linksEndContainer.classList.contains("with-query")).toBe(true);
    });

    it("does not add 'with-query' class when queryText is empty", () => {
        createUI(linksEndContainer, 5, "");

        expect(linksEndContainer.classList.contains("with-query")).toBe(false);
    });

    it("creates left, query, and right wrappers inside linksEndContainer", () => {
        createUI(linksEndContainer, 3, "foo");

        const leftWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__left-wrapper",
        );
        const queryWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__query-wrapper",
        );
        const rightWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__right-wrapper",
        );

        expect(leftWrapper).not.toBeNull();
        expect(queryWrapper).not.toBeNull();
        expect(rightWrapper).not.toBeNull();
    });

    it("creates prev and next links with correct attributes", () => {
        const { prevLink, nextLink } = createUI(
            linksEndContainer,
            10,
            "search",
        );

        expect(prevLink).not.toBeNull();
        expect(prevLink.tagName).toBe("A");
        expect(prevLink.textContent).toBe("Previous");
        expect(prevLink.getAttribute("href")).toBe("#");
        expect(
            prevLink.classList.contains("document-navigation-links__link-left"),
        ).toBe(true);
        expect(prevLink.title).toBe("Previous match");

        expect(nextLink).not.toBeNull();
        expect(nextLink.tagName).toBe("A");
        expect(nextLink.textContent).toBe("Next");
        expect(nextLink.getAttribute("href")).toBe("#");
        expect(
            nextLink.classList.contains(
                "document-navigation-links__link-right",
            ),
        ).toBe(true);
        expect(nextLink.title).toBe("Next match");

        const leftWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__left-wrapper",
        );
        const rightWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__right-wrapper",
        );

        expect(leftWrapper.contains(prevLink)).toBe(true);
        expect(rightWrapper.contains(nextLink)).toBe(true);
    });

    it("renders query label when queryText is provided", () => {
        createUI(linksEndContainer, 7, "lorem ipsum");

        const queryLabelContainer = linksEndContainer.querySelector(
            ".document-navigation-links__search-query-text-container.document-navigation-links__query",
        );
        const queryTextSpan = linksEndContainer.querySelector(
            ".document-navigation-links__query-text",
        );

        expect(queryLabelContainer).not.toBeNull();
        expect(queryLabelContainer.textContent.startsWith("Query: ")).toBe(
            true,
        );
        expect(queryTextSpan.textContent).toBe("lorem ipsum");
    });

    it("omits query label when queryText is empty but still shows match count", () => {
        createUI(linksEndContainer, 4, "");

        const queryLabelContainer = linksEndContainer.querySelector(
            ".document-navigation-links__search-query-text-container.document-navigation-links__query",
        );
        const matchCountWrapper = linksEndContainer.querySelector(
            ".document-navigation-links__match-count-wrapper.document-navigation-links__matches",
        );

        expect(queryLabelContainer).toBeNull();
        expect(matchCountWrapper).not.toBeNull();
    });

    it("sets total match count correctly in the match count wrapper", () => {
        createUI(linksEndContainer, 42, "needle");

        const countSpan = linksEndContainer.querySelector(
            ".document-navigation-links__match-count.document-navigation-links__link-count",
        );

        expect(countSpan).not.toBeNull();
        expect(countSpan.textContent).toBe("42");
    });

    it("returns a positionSpan that matches the DOM and is initially empty", () => {
        const { positionSpan } = createUI(linksEndContainer, 5, "query");

        const domPositionSpan = linksEndContainer.querySelector(
            ".document-navigation-links__match-position.position",
        );

        expect(positionSpan).not.toBeNull();
        expect(positionSpan).toBe(domPositionSpan);
        expect(positionSpan.textContent).toBe("");
    });
});
