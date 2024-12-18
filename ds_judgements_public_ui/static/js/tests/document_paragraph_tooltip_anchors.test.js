import { describe, expect, it, jest } from "@jest/globals";

import {
    isMobile,
    getTooltipPositionClass,
    createAnchorElement,
    copyLinkToClipboard,
    createCopyElement,
    createCopyableAnchorElement,
    addDocumentParagraphAnchorLinkToSection,
    removeDocumentParagraphAnchorLinkFromSection,
} from "../src/document_paragraph_tooltip_anchors";

const setWindowInnerWidth = (width) => {
    Object.defineProperty(window, "innerWidth", {
        writeable: true,
        configurable: true,
        value: width,
    });
};

describe("isMobile", () => {
    it("returns true if window.innerWidth is less than 1135", () => {
        setWindowInnerWidth(1134);
        expect(isMobile()).toBe(true);
    });

    it("returns false if window.innerWidth is 1135 or greater", () => {
        setWindowInnerWidth(1135);
        expect(isMobile()).toBe(false);
    });
});

describe("getTooltipPositionClass", () => {
    it("returns the top tooltip class on mobile", () => {
        setWindowInnerWidth(1134);
        expect(getTooltipPositionClass()).toBe(
            "judgment-body__copy-link-tooltip--top",
        );
    });

    it("returns the left tooltip class on desktop", () => {
        setWindowInnerWidth(1135);
        expect(getTooltipPositionClass()).toBe(
            "judgment-body__copy-link-tooltip--left",
        );
    });
});

describe("createAnchorElement", () => {
    it("creates an anchor element with the correct attributes and content", () => {
        const element = createAnchorElement("test-id", "Test content");

        expect(element.tagName).toBe("A");
        expect(element.href).toContain("#test-id");
        expect(element.classList.contains("judgment-body__anchor-link")).toBe(
            true,
        );
        expect(element.textContent).toBe("Test content");
    });
});

describe("copyLinkToClipboard", () => {
    it("copies text to clipboard", () => {
        const mockEvent = {
            preventDefault: jest.fn(),
            stopPropagation: jest.fn(),
        };
        const mockWriteText = jest.fn();
        navigator.clipboard = { writeText: mockWriteText };

        copyLinkToClipboard(mockEvent, "Test text");
        expect(mockWriteText).toHaveBeenCalledWith("Test text");
    });
});

describe("createCopyElement", () => {
    it("creates an element with copy functionality", () => {
        setWindowInnerWidth(1135);
        const element = createCopyElement("Test text");

        expect(element.tagName).toBe("SPAN");
        expect(
            element.classList.contains("judgment-body__copy-link-tooltip"),
        ).toBe(true);
        expect(element.textContent).toBe("Copy link to this paragraph");

        const mockEvent = {
            preventDefault: jest.fn(),
            stopPropagation: jest.fn(),
        };
        const mockWriteText = jest.fn();
        navigator.clipboard = { writeText: mockWriteText };

        element.click(mockEvent);

        expect(mockWriteText).toHaveBeenCalledWith("Test text");
        expect(element.textContent).toBe("Copied!");
    });
});

describe("createCopyableAnchorElement", () => {
    it("creates an anchor element with copy functionality", () => {
        setWindowInnerWidth(1135);
        const element = createCopyableAnchorElement("test-id", "Test content");

        expect(element.tagName).toBe("A");
        expect(element.href).toContain("#test-id");
        expect(
            element.querySelector(".judgment-body__copy-link-tooltip"),
        ).toBeTruthy();
    });
});

describe("addDocumentParagraphAnchorLinkToSection", () => {
    it("adds a copyable anchor link to a section", () => {
        document.body.innerHTML = `
            <div id="test-section" class="judgment-body__section">
                <span class="judgment-body__number">123</span>
            </div>
        `;
        const section = document.getElementById("test-section");

        addDocumentParagraphAnchorLinkToSection(section);

        const numberElement = section.querySelector(".judgment-body__number");
        expect(numberElement.dataset.numberContent).toBe("123");
        expect(numberElement.querySelector("a")).toBeTruthy();
    });

    it("does nothing if section is invalid", () => {
        expect(() =>
            addDocumentParagraphAnchorLinkToSection(null),
        ).not.toThrow();
    });
});

describe("removeDocumentParagraphAnchorLinkFromSection", () => {
    it("removes anchor link and restores original content", () => {
        document.body.innerHTML = `
            <div id="test-section" class="judgment-body__section">
                <span class="judgment-body__number" data-number-content="123">
                    <a href="#test-section">123</a>
                </span>
            </div>
        `;
        const section = document.getElementById("test-section");

        removeDocumentParagraphAnchorLinkFromSection(section);

        const numberElement = section.querySelector(".judgment-body__number");
        expect(numberElement.innerHTML).toBe("123");
    });
});
