import { beforeEach, describe, expect, it, jest } from "@jest/globals";

import { setupSearchResultsControls } from "../src/search_results_controls";

describe("setupSearchResultsControls", () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div>
                <form data-search-results-controls>
                    <input name="query" value="example" />
                    <select name="order"><option value="date">Oldest</option></select>
                    <select name="per_page"><option value="25">25</option></select>
                    <input type="submit" value="Sort" />
                    <input type="submit" value="Apply" />
                </form>
            </div>
            <div>
                <form data-search-results-controls>
                    <select name="per_page"><option value="50">50</option></select>
                    <input type="submit" value="Apply" />
                </form>
            </div>`;
    });

    it("leaves buttons available until JavaScript enhances the controls", () => {
        const buttons = [...document.querySelectorAll("[type='submit']")];
        expect(buttons.every((button) => !button.hidden)).toBe(true);

        setupSearchResultsControls();

        expect(buttons.every((button) => button.hidden)).toBe(true);
    });

    it.each(["order", "per_page"])(
        "submits the top form when %s changes",
        (name) => {
            const form = document.querySelector("form");
            form.requestSubmit = jest.fn();
            setupSearchResultsControls();

            form.querySelector(`select[name='${name}']`).dispatchEvent(
                new Event("change"),
            );

            expect(form.requestSubmit).toHaveBeenCalledTimes(1);
            expect(new FormData(form).get("query")).toBe("example");
        },
    );

    it("submits only the footer form when its page size changes", () => {
        const [top, footer] = document.querySelectorAll("form");
        top.requestSubmit = jest.fn();
        footer.requestSubmit = jest.fn();
        setupSearchResultsControls();

        footer.querySelector("select").dispatchEvent(new Event("change"));

        expect(footer.requestSubmit).toHaveBeenCalledTimes(1);
        expect(top.requestSubmit).not.toHaveBeenCalled();
    });
});
