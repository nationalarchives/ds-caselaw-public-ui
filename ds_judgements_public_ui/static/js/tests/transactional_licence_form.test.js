import { describe, expect, it, beforeEach, jest } from "@jest/globals";

import {
    setupTogglableFields,
    setupPreviousButton,
    goToFirstErrorField,
} from "../src/transactional_licence_form";

describe("setupTogglableFields", () => {
    beforeEach(() => {
        document.body.innerHTML = `
      <div id="div_id_contact-licence_holder_lastname" style="display: none;"></div>
      <div id="div_id_contact-licence_holder_email" style="display: none;"></div>
      <div id="div_id_contact-alternative_contact">
        <input type="radio" value="Yes" name="contact-alternative_contact" />
        <input type="radio" value="No" name="contact-alternative_contact" />
      </div>
    `;
    });

    it("shows fields when 'Yes' is selected", () => {
        setupTogglableFields();

        const yesRadio = document.querySelector(
            "#div_id_contact-alternative_contact input[value='Yes']",
        );
        yesRadio.checked = true;
        yesRadio.dispatchEvent(new Event("change"));

        expect(
            getComputedStyle(
                document.querySelector(
                    "#div_id_contact-licence_holder_lastname",
                ),
            ).display,
        ).toBe("block");
        expect(
            getComputedStyle(
                document.querySelector("#div_id_contact-licence_holder_email"),
            ).display,
        ).toBe("block");
    });

    it("hides fields when 'No' is selected", () => {
        setupTogglableFields();

        const noRadio = document.querySelector(
            "#div_id_contact-alternative_contact input[value='No']",
        );
        noRadio.checked = true;
        noRadio.dispatchEvent(new Event("change"));

        expect(
            getComputedStyle(
                document.querySelector(
                    "#div_id_contact-licence_holder_lastname",
                ),
            ).display,
        ).toBe("none");
        expect(
            getComputedStyle(
                document.querySelector("#div_id_contact-licence_holder_email"),
            ).display,
        ).toBe("none");
    });
});

describe("setupPreviousButton", () => {
    beforeEach(() => {
        document.body.innerHTML = `
      <form id="transactional-licence-form-form">
        <button
          id="transactional-licence-form-previous-button"
          type="button"
          name="wizard_goto_step"
          value="previous-page"
        >
          Previous
        </button>
      </form>
    `;

        document.querySelector("form").requestSubmit = jest.fn();
    });

    it("shows the 'Previous' button", () => {
        setupPreviousButton();

        const button = document.getElementById(
            "transactional-licence-form-previous-button",
        );
        expect(button.style.display).toBe("inline");
    });
});

describe("previous button submission", () => {
    it("includes the previous step when submitting the form", () => {
        document.body.innerHTML =
            '<form id="transactional-licence-form-form"><button type="button" id="transactional-licence-form-previous-button" name="wizard_goto_step" value="contact">Previous</button></form>';
        const form = document.querySelector("form");
        form.requestSubmit = jest.fn();
        setupPreviousButton();
        document.querySelector("button").click();
        expect(form.requestSubmit).toHaveBeenCalledTimes(1);
        expect(new FormData(form).get("wizard_goto_step")).toBe("contact");
    });
});

describe("goToFirstErrorField", () => {
    beforeEach(() => {
        document.body.innerHTML = `
          <div style="margin-top: 500px;" class="govuk-error-message" tabindex="-1">This is an error</div>
    `;
        window.scrollTo = jest.fn();
    });

    it("scrolls to the error-message and focuses it", () => {
        goToFirstErrorField();

        expect(document.activeElement).toBe(
            document.querySelector(".govuk-error-message"),
        );
        expect(window.scrollTo).toHaveBeenCalledWith({
            top: -80,
            behavior: "instant",
        });
    });

    it("does not scroll or focus when there are no errors", () => {
        document.body.innerHTML = "<form><input /></form>";

        expect(() => goToFirstErrorField()).not.toThrow();

        expect(window.scrollTo).not.toHaveBeenCalled();
    });

    it("focuses only the first error when there are multiple errors", () => {
        document.body.innerHTML +=
            '<div class="govuk-error-message">Another error</div>';

        goToFirstErrorField();

        expect(document.activeElement).toBe(
            document.querySelector(".govuk-error-message"),
        );
    });
});
