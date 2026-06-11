import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Radios",
    render: renderLoadedHtml,
};

const docs = `
  {{ radios({
    "idPrefix": "radios",
    "name": "radios",
    "hint": {
      "text": "This is the hint text"
    },
    "items": [
      {
        "value": "option1",
        "text": "Option 1"
      },
      {
        "value": "option2",
        "text": "Option 2"
      },
      {
        "value": "option3",
        "text": "Option 3"
      }
    ]
  }) }}
`;

export const Radios = createExampleStory(
    "components/radios.jinja",
    "radios_examples",
    docs,
);
