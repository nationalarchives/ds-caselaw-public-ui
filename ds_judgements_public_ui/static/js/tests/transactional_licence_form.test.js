import { describe, expect, it, beforeEach, jest } from "@jest/globals";

import $ from "jquery";
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

        $.fn.show = jest.fn(function () {
            this.css("display", "block");
        });
        $.fn.hide = jest.fn(function () {
            this.css("display", "none");
        });
    });

    it("shows fields when 'Yes' is selected", () => {
        setupTogglableFields();

        const yesRadio = $(
            "#div_id_contact-alternative_contact input[value='Yes']",
        )[0];
        yesRadio.checked = true;
        $(yesRadio).trigger("change");

        expect(
            $("#div_id_contact-licence_holder_lastname").css("display"),
        ).toBe("block");
        expect($("#div_id_contact-licence_holder_email").css("display")).toBe(
            "block",
        );
    });

    it("hides fields when 'No' is selected", () => {
        setupTogglableFields();

        const noRadio = $(
            "#div_id_contact-alternative_contact input[value='No']",
        )[0];
        noRadio.checked = true;
        $(noRadio).trigger("change");

        expect(
            $("#div_id_contact-licence_holder_lastname").css("display"),
        ).toBe("none");
        expect($("#div_id_contact-licence_holder_email").css("display")).toBe(
            "none",
        );
    });
});

describe("setupPreviousButton", () => {
    beforeEach(() => {
        document.body.innerHTML = `
      <form id="transactional-licence-form-form">
        <button
          id="transactional-licence-form-previous-button"
          name="previous"
          value="previous-page"
        >
          Previous
        </button>
      </form>
    `;

        $.fn.prependTo = jest.fn();
        $.fn.trigger = jest.fn();
    });

    it("shows the 'Previous' button", () => {
        setupPreviousButton();

        const button = document.getElementById(
            "transactional-licence-form-previous-button",
        );
        expect(button.style.display).toBe("inline");
    });
});

describe("goToFirstErrorField", () => {
    beforeEach(() => {
        document.body.innerHTML = `
          <div style="margin-top: 500px;" class="govuk-error-message" tabindex="-1">This is an error</div>
    `;
        $.fn.animate = function (props, duration, callback) {
            callback();
            return this;
        };

        $.fn.focus = jest.fn();
    });

    it("scrolls to the error-message and focuses it", () => {
        goToFirstErrorField();

        expect($.fn.focus).toHaveBeenCalled();
    });
});
