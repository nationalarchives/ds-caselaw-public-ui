import { createExampleStory, renderLoadedHtml } from "../helpers.js";

export default {
    title: "Components/Documents table",
    render: renderLoadedHtml,
};

const docs = `
  {% call documents_table(title="Recently published judgments", headings=["Neutral citation", "Handed down"]) %}
    {% call document_table_row() %}
      {% call document_table_cell(variant="details") %}
        <a href="">Laurence Pagden & Anor v Craig Andrew Ridgley</a>
        High Court (Insolvency and Companies List)
      {% endcall %}
      {% call document_table_cell(variant="text", label="Neutral citation") %}
        [2025] EWHC 2674 (Ch)
      {% endcall %}
      {% call document_table_cell(variant="text", label="Handed down") %}
        17 Oct 2025
      {% endcall %}
    {% endcall %}
  {% endcall %}
`;

export const DocumentsTable = createExampleStory(
    "components/documents_table.jinja",
    "documents_table_examples",
    docs,
);
