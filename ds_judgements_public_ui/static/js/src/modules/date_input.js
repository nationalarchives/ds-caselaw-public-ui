import $ from "jquery";

function constrainInputToMinMax() {
    const input = $(this);
    var lastValidValue = input.value;
    input.on("input", (event) => {
        const validity = input[0].validity;
        if (validity.badInput) {
            this.value = lastValidValue;
        } else if (validity.rangeOverflow) {
            this.value = this.max;
        } else {
            lastValidValue = this.value;
        }
    });
}

function setupDateInput() {
    const wrapper = $(this);
    const inputs = wrapper.find("input");
    inputs.each(constrainInputToMinMax);
}

$(() => {
    //$(".js-date-input").each(setupDateInput);
});
