export function setupSearchResultsControls() {
    document
        .querySelectorAll("[data-search-results-controls]")
        .forEach((form) => {
            form.querySelectorAll(
                "select[name='order'], select[name='per_page']",
            ).forEach((select) => {
                select.addEventListener("change", () => form.requestSubmit());
            });
            form.querySelectorAll("[type='submit']").forEach((button) => {
                button.hidden = true;
            });
        });
}
