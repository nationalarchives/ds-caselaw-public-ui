import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Select",
    render: renderLoadedHtml,
};

const docs = `
  {{ govukSelect({
    "id": "country",
    "name": "country",
    "label": {
      "text": "Label text"
    },
    "hint": {
      "text": "This is the hint text"
    },
    "disabled": false,
    "items": [
      {
        "text": "Select an option",
        "value": "",
        "selected": true,
        "disabled": true
      },
      {
        "text": "Option 1",
        "value": "option1"
      },
      {
        "text": "Option 2",
        "value": "option2"
      },
      {
        "text": "Option 3",
        "value": "option3"
      }
    ]
  }) }}
`;

export const Select = createExampleStory(
    "components/select.jinja",
    "select_examples",
    docs,
);
