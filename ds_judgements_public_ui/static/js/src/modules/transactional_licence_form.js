import $ from "jquery";

/*  CAUTION: This is quite a specific and brittle way of addressing these
    particular form fields, but Django-forms doesn't give us many
    other options: I haven't found a way to simply add an id or
    class to a single radio button or checkbox input. If the values or names
    of these form fields change, this code will also have to change.
*/
var licenceHolderNameId = "div_id_contact-licence_holder_lastname";
var licenceHolderEmailId = "div_id_contact-licence_holder_email";
var licenceHolderControlSelector = "#div_id_contact-alternative_contact input";
var licenceHolderVisibleValue =
    "This is a different person (please enter their details below)";

$(`#${licenceHolderNameId}`).hide();
$(`#${licenceHolderEmailId}`).hide();
$(licenceHolderControlSelector).attr(
    "aria-controls",
    `${licenceHolderNameId} ${licenceHolderEmailId}`,
);
$(licenceHolderControlSelector).attr("aria-expanded", false);
$(function () {
    $(licenceHolderControlSelector).change(function (event) {
        if (this.value == licenceHolderVisibleValue) {
            $(licenceHolderControlSelector).attr("aria-expanded", true);
            $(`#${licenceHolderNameId}`).show();
            $(`#${licenceHolderEmailId}`).show();
        } else {
            $(licenceHolderControlSelector).attr("aria-expanded", false);
            $(`#${licenceHolderNameId}`).hide();
            $(`#${licenceHolderEmailId}`).hide();
        }
    });
});
