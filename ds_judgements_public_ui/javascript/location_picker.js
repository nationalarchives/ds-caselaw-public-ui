import openregisterLocationPicker from "govuk-country-and-territory-autocomplete";

document.querySelectorAll(".location-autocomplete").forEach(function (select) {
    openregisterLocationPicker({
        selectElement: select,
        url: "/static/js/location-autocomplete-canonical-list.json",
    });
});
