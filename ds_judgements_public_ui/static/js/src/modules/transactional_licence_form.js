import $ from "jquery";

let setupTogglableFields = function () {
    /*  CAUTION: This is quite a specific and brittle way of addressing these
        particular form fields, but Django-forms doesn't give us many
        other options: I haven't found a way to simply add an id or
        class to a single radio button or checkbox input. If the values or names
        of these form fields change, this code will also have to change.
    */
    var licenceHolderNameId = "div_id_contact-licence_holder_lastname";
    var licenceHolderEmailId = "div_id_contact-licence_holder_email";
    var licenceHolderControlSelector =
        "#div_id_contact-alternative_contact input";
    var licenceHolderVisibleValue = "Yes";

    let toggleFieldState = function (element) {
        if (element && element.value == licenceHolderVisibleValue) {
            showFields();
        } else {
            hideFields();
        }
    };

    let showFields = function () {
        $(licenceHolderControlSelector).attr("aria-expanded", true);
        $(`#${licenceHolderNameId}`).show();
        $(`#${licenceHolderEmailId}`).show();
    };

    let hideFields = function () {
        $(licenceHolderControlSelector).attr("aria-expanded", false);
        $(`#${licenceHolderNameId}`).hide();
        $(`#${licenceHolderEmailId}`).hide();
    };

    $(licenceHolderControlSelector).attr(
        "aria-controls",
        `${licenceHolderNameId} ${licenceHolderEmailId}`,
    );

    toggleFieldState($(`${licenceHolderControlSelector}:checked`)[0]);

    $(licenceHolderControlSelector).change(function (event) {
        toggleFieldState(this);
    });
};

let setupPreviousButton = function () {
    /*
        This is handled with javascript for a couple of intersecting reasons.
        For accesibility compliance, pressing enter while on a form field should take you
        to the next page of the form. However, by default, pressing enter submits using the *first*
        button with type "submit" in the form, which in our case, would have been the "previous" button:
       https://stackoverflow.com/questions/48/multiple-submit-buttons-in-an-html-form

       One way around this is to reverse the order of the buttons in the markup, and then to float them right,
       however, this causes another accessibility problem: the tabbing order for those buttons is then reversed in
       a confusing way.

       To fix this, we give the "previous" button the type "button", and submit it using javascript, that way the
       first "submit" button in the form is the correct "default" action of going to the next page.
    */
    let button = document.getElementById(
        "transactional-licence-form-previous-button",
    );
    let form = document.getElementById("transactional-licence-form-form");
    if (button) {
        button.style.display = "inline";
        $(button).click(function (e) {
            e.preventDefault();
            $("<input type='hidden' />")
                .attr("name", button.getAttribute("name"))
                .attr("value", button.getAttribute("value"))
                .prependTo(form);
            $(form).trigger("submit");
        });
    }
};

$(function () {
    setupTogglableFields();
    setupPreviousButton();
});
