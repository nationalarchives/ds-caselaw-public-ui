import { setupSearchResultsControls } from "./search_results_controls";

export function manageFilters(wrapper, options = {}) {
    const settings = { ...manageFilters.defaults, ...options };
    const toggleArea = wrapper.querySelector(".js-results-facets");
    const controlContainer = wrapper.querySelector(
        ".js-results-control-container",
    );
    if (!toggleArea || !controlContainer) return;
    const filters = wrapper.querySelector(".js-results-facets-applied-filters");
    const button = document.createElement("button");
    button.className = "results-search-component__toggle-control collapsed";
    button.type = "button";
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", "js-results-facets");
    const collapsedText = () =>
        (filters?.children.length ?? 0) === 0
            ? settings.collapsed_text_without_filters
            : settings.collapsed_text_with_filters;
    button.textContent = collapsedText();

    button.addEventListener("click", () => {
        toggleArea.style.display =
            getComputedStyle(toggleArea).display === "none" ? "block" : "none";
        const collapsed = button.classList.toggle("collapsed");
        button.setAttribute("aria-expanded", String(!collapsed));
        button.textContent = collapsed
            ? collapsedText()
            : settings.expanded_text;
    });
    controlContainer.append(button);
}

manageFilters.defaults = {
    collapsed_text_with_filters: "Add another filter",
    collapsed_text_without_filters: "Filter by court, date or person",
    expanded_text: "Hide filter options",
};

document
    .querySelectorAll(".js-results-facets-wrapper")
    .forEach((wrapper) => manageFilters(wrapper));
setupSearchResultsControls();
