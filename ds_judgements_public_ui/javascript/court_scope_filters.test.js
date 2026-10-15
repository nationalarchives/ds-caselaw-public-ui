import { beforeEach, describe, expect, it } from "@jest/globals";
import { setupCourtScopeFilters } from "./court_scope_filters";

describe("court scope filters", () => {
    beforeEach(() => {
        document.body.innerHTML = `<form><fieldset data-court-scope>
          <input type="checkbox" name="scope" value="higher_courts" data-scope-toggle>
          <span data-scope-label>Select all</span>
          <div data-court-group>
            <input type="checkbox" data-group-toggle hidden>
            <input type="checkbox" name="court" value="ewca/civ">
            <input type="checkbox" name="court" value="ewca/crim">
          </div>
          <input type="checkbox" name="court" value="uksc">
        </fieldset><fieldset data-court-scope>
          <input type="checkbox" name="scope" value="other_courts" data-scope-toggle>
          <span data-scope-label>Select all</span>
          <div data-court-group>
            <input type="checkbox" data-group-toggle hidden>
            <input type="checkbox" name="court" value="eat">
          </div>
          <input type="checkbox" name="court" value="ewcc">
        </fieldset></form>`;
        setupCourtScopeFilters();
    });

    it("selects and deselects all courts and changes the label", () => {
        const toggle = document.querySelector("[data-scope-toggle]");
        toggle.click();
        expect(
            document.querySelectorAll('input[name="court"]:checked'),
        ).toHaveLength(3);
        expect(document.querySelector("[data-scope-label]").textContent).toBe(
            "Deselect all",
        );
        toggle.click();
        expect(
            document.querySelectorAll('input[name="court"]:checked'),
        ).toHaveLength(0);
        expect(document.querySelector("[data-scope-label]").textContent).toBe(
            "Select all",
        );
    });

    it("toggles a group and updates partial selection states", () => {
        const group = document.querySelector("[data-group-toggle]");
        expect(group.hidden).toBe(false);
        group.click();
        expect(
            document.querySelectorAll('input[name="court"]:checked'),
        ).toHaveLength(2);
        expect(
            document.querySelector("[data-scope-toggle]").indeterminate,
        ).toBe(true);
        document.querySelector('input[value="ewca/civ"]').click();
        expect(group.checked).toBe(false);
        expect(group.indeterminate).toBe(true);
    });

    it("combines both scopes into all courts on submission", () => {
        document.querySelector("[data-scope-toggle]").click();
        document.querySelector('input[value="other_courts"]').click();
        const form = document.querySelector("form");
        const data = new FormData(form);
        const event = new Event("formdata");
        event.formData = data;
        form.dispatchEvent(event);
        expect(data.getAll("scope")).toEqual(["all_courts"]);
        expect(data.getAll("court")).toEqual([]);
    });

    it("removes individual courts from scoped submissions", () => {
        document.querySelector("[data-scope-toggle]").click();
        const form = document.querySelector("form");
        const data = new FormData(form);
        const event = new Event("formdata");
        event.formData = data;
        form.dispatchEvent(event);
        expect(data.getAll("scope")).toEqual(["higher_courts"]);
        expect(data.getAll("court")).toEqual([]);
    });

    it.each([
        ["higher_courts", "eat", ["ewca/civ", "ewca/crim", "uksc", "eat"]],
        ["other_courts", "uksc", ["uksc", "eat", "ewcc"]],
    ])(
        "submits courts when %s is combined with %s",
        (scope, court, expected) => {
            document.querySelector(`input[value="${scope}"]`).click();
            document.querySelector(`input[value="${court}"]`).click();
            const form = document.querySelector("form");
            const data = new FormData(form);
            const event = new Event("formdata");
            event.formData = data;
            form.dispatchEvent(event);
            expect(data.getAll("scope")).toEqual([]);
            expect(data.getAll("court")).toEqual(expected);
        },
    );

    it("submits courts when a group outside the selected scope is checked", () => {
        document.querySelector('input[value="higher_courts"]').click();
        document
            .querySelectorAll("[data-court-scope]")[1]
            .querySelector("[data-group-toggle]")
            .click();
        const form = document.querySelector("form");
        const data = new FormData(form);
        const event = new Event("formdata");
        event.formData = data;
        form.dispatchEvent(event);
        expect(data.getAll("scope")).toEqual([]);
        expect(data.getAll("court")).toEqual([
            "ewca/civ",
            "ewca/crim",
            "uksc",
            "eat",
        ]);
    });

    it("uses the scope again after the additional court is deselected", () => {
        document.querySelector('input[value="higher_courts"]').click();
        const court = document.querySelector('input[value="eat"]');
        court.click();
        court.click();
        const form = document.querySelector("form");
        const data = new FormData(form);
        const event = new Event("formdata");
        event.formData = data;
        form.dispatchEvent(event);
        expect(data.getAll("scope")).toEqual(["higher_courts"]);
        expect(data.getAll("court")).toEqual([]);
    });
});
