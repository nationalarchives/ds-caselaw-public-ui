import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Pagination",
    render: renderLoadedHtml,
};

const docs = `
  {{ pagination({
    "previous": {
      "href": "?page=4",
      "html": "Previous"
    },
    "items": [
      {
        "number": 1,
        "href": "?page=1"
      },
      {
        "ellipsis": true
      },
      {
        "number": 4,
        "href": "?page=4"
      },
      {
        "number": 5,
        "href": "?page=5",
        "current": true
      },
      {
        "number": 6,
        "href": "?page=6"
      },
      {
        "ellipsis": true
      },
      {
        "number": 12,
        "href": "?page=12"
      }
    ],
    "next": {
      "href": "?page=6",
      "html": "Next"
    }
  }) }}
`;

export const Pagination = createExampleStory(
    "components/pagination.jinja",
    "pagination_examples",
    docs,
);
