import { describe, expect, it, beforeEach } from "@jest/globals";

import { manageFilters } from "./manage_filters";

describe("manage_filters", () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div class="js-results-facets-wrapper">
                <div class="js-results-control-container"></div>
                <div class="js-results-facets" style="display: none"></div>
                <div class="js-results-facets-applied-filters"></div>
            </div>
        `;
    });

    it("initialises the button with correct text when there are no filters", () => {
        manageFilters(document.querySelector(".js-results-facets-wrapper"));
        const button = document.querySelector(
            ".results-search-component__toggle-control",
        );

        expect(button).not.toBeNull();
        expect(button.textContent).toBe("Filter by court, date or person");
        expect(button.getAttribute("aria-expanded")).toBe("false");
    });

    it("initialises the button when filters are applied", () => {
        document.querySelector(".js-results-facets-applied-filters").innerHTML =
            `<div class="filter-item">Filter 1</div>`;

        manageFilters(document.querySelector(".js-results-facets-wrapper"));
        const button = document.querySelector(
            ".results-search-component__toggle-control",
        );

        expect(button).not.toBeNull();
        expect(button.textContent).toBe("Add another filter");
        expect(button.getAttribute("aria-expanded")).toBe("false");
    });

    it("toggles the filter section on click", () => {
        manageFilters(document.querySelector(".js-results-facets-wrapper"));

        const button = document.querySelector(
            ".results-search-component__toggle-control",
        );
        const toggleArea = document.querySelector(".js-results-facets");

        expect(button.getAttribute("aria-expanded")).toBe("false");
        expect(button.classList.contains("collapsed")).toBe(true);
        expect(toggleArea.style.display).toBe("none");

        button.click();

        expect(button.getAttribute("aria-expanded")).toBe("true");
        expect(button.classList.contains("collapsed")).toBe(false);
        expect(toggleArea.style.display).toBe("block");

        button.click();

        expect(button.getAttribute("aria-expanded")).toBe("false");
        expect(button.classList.contains("collapsed")).toBe(true);
        expect(toggleArea.style.display).toBe("none");
    });

    it("updates the button text based on the presence of filters", () => {
        manageFilters(document.querySelector(".js-results-facets-wrapper"));
        const button = document.querySelector(
            ".results-search-component__toggle-control",
        );

        expect(button.textContent).toBe("Filter by court, date or person");

        const filters = document.querySelector(
            ".js-results-facets-applied-filters",
        );

        filters.innerHTML = `<div class="filter-item">Filter 1</div>`;
        button.click();

        expect(button.textContent).toBe("Hide filter options");
    });
});
