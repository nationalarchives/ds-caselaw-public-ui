import { describe, expect, it, beforeEach, jest } from "@jest/globals";

import {
    copyLinkToClipboard,
    createTooltipElement,
    addCopyLinkTooltip,
    setupCopyLinkTooltips,
} from "../src/copy_link_tooltip";

describe("copyLinkToClipboard", () => {
    beforeEach(() => {
        Object.assign(navigator, {
            clipboard: {
                writeText: jest.fn(),
            },
        });
    });

    it("writes to the clipboard", () => {
        const event = {
            preventDefault: jest.fn(),
            stopPropagation: jest.fn(),
        };

        const textToCopy = "https://example.com";

        copyLinkToClipboard(event, textToCopy);

        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(textToCopy);
    });
});

describe("createTooltipElement", () => {
    it("creates a tooltip element with the given text", () => {
        const text = "Copy me";

        const tooltip = createTooltipElement(text);

        expect(tooltip.tagName).toBe("SPAN");
        expect(
            tooltip.classList.contains("copy-to-clipboard-link__tooltip"),
        ).toBe(true);
        expect(tooltip.innerHTML).toBe(text);
    });
});

describe("addCopyLinkTooltip", () => {
    let link;

    beforeEach(() => {
        link = document.createElement("a");
        link.href = "https://example.com";
        link.dataset.copyLinkTooltip = "Copy me";
        document.body.appendChild(link);

        Object.assign(navigator, {
            clipboard: {
                writeText: jest.fn(),
            },
        });
    });

    afterEach(() => {
        document.body.innerHTML = "";
    });

    it("adds a tooltip and click event listener to the link", () => {
        addCopyLinkTooltip(link);

        const tooltip = link.querySelector(".copy-to-clipboard-link__tooltip");
        expect(tooltip).not.toBeNull();
        expect(tooltip.innerHTML).toBe("Copy me");

        link.click();

        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(link.href);
        expect(tooltip.innerHTML).toBe("Copied!");

        jest.advanceTimersByTime(3000);
        expect(tooltip.innerHTML).toBe("Copy me");
    });

    it("does nothing if the link is invalid", () => {
        const invalidLink = null;
        expect(() => addCopyLinkTooltip(invalidLink)).not.toThrow();
    });
});

describe("setupCopyLinkTooltips", () => {
    beforeEach(() => {
        const link1 = document.createElement("a");
        link1.href = "https://example.com";
        link1.dataset.copyLinkTooltip = "Copy me";

        const link2 = document.createElement("a");
        link2.href = "https://another.com";
        link2.dataset.copyLinkTooltip = "Also copy me";

        document.body.appendChild(link1);
        document.body.appendChild(link2);

        Object.assign(navigator, {
            clipboard: {
                writeText: jest.fn(),
            },
        });
    });

    afterEach(() => {
        document.body.innerHTML = "";
    });

    it("initialises tooltips for all links with the data-copy-link-tooltip attribute", () => {
        setupCopyLinkTooltips();

        const links = document.querySelectorAll("[data-copy-link-tooltip]");

        links.forEach((link) => {
            const tooltip = link.querySelector(
                ".copy-to-clipboard-link__tooltip",
            );
            expect(tooltip).not.toBeNull();
        });
    });
});
