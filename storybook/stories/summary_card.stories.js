import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/SummaryCard",
    render: renderLoadedHtml,
};

const docs = `
  {{ summary_card({
    "card": {
      "title": {
        "text": "This is the title text"
      }
    },
    "rows": [
      {
        "key": {
          "text": "This is the key text"
        },
        "value": {
          "html": "This is the value text"
        },
        "actions": {
          "items": [
            {
              "href": "#",
              "text": "Change",
              "visuallyHiddenText": "This is the hidden key text"
            }
          ]
        }
      },
      {
        "key": {
          "text": "This is the key text"
        },
        "value": {
          "html": "This is the value text"
        },
        "actions": {
          "items": [
            {
              "href": "#",
              "text": "Change",
              "visuallyHiddenText": "This is the hidden key text"
            }
          ]
        }
      },
      {
        "key": {
          "text": "This is the key text"
        },
        "value": {
          "html": "This is the value text"
        },
        "actions": {
          "items": [
            {
              "href": "#",
              "text": "Change",
              "visuallyHiddenText": "This is the hidden key text"
            }
          ]
        }
      }
    ]
  }) }}
`;

export const SummaryCard = createExampleStory(
    "components/summary_card.jinja",
    "summary_card_examples",
    docs,
);
