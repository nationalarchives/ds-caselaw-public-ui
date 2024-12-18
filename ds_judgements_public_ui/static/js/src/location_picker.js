import $ from "jquery";
import openregisterLocationPicker from "govuk-country-and-territory-autocomplete";

$(".location-autocomplete").each(function (ix) {
    openregisterLocationPicker({
        selectElement: this,
        url: "/static/js/location-autocomplete-canonical-list.json",
    });
});
