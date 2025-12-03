import { describe, expect, it, beforeEach } from "@jest/globals";
import {
    getQueryFromUrl,
    getMarksInDocumentBody,
} from "../../src/document_search_links/utils";

describe("getQueryFromUrl", () => {
    beforeEach(() => {
        window.history.pushState({}, "", "/");
    });

    it("returns an empty string if there is no query parameter", () => {
        expect(getQueryFromUrl()).toBe("");
    });

    it("returns the value of the default 'query' parameter", () => {
        window.history.pushState({}, "", "/?query=hello");
        expect(getQueryFromUrl()).toBe("hello");
    });

    it("returns the value of a custom parameter name", () => {
        window.history.pushState({}, "", "/?search=abc");
        expect(getQueryFromUrl("search")).toBe("abc");
    });

    it("returns an empty string if the specified parameter is missing", () => {
        window.history.pushState({}, "", "/?query=xyz");
        expect(getQueryFromUrl("notfound")).toBe("");
    });
});

describe("getMarksInDocumentBody", () => {
    beforeEach(() => {
        document.body.innerHTML = "";
    });

    it("returns an empty array if there is no [data-document-body] element", () => {
        const result = getMarksInDocumentBody();
        expect(result).toEqual([]);
    });

    it("returns an empty array if the container has no <mark> elements", () => {
        document.body.innerHTML = `<div data-document-body><p>No marks here</p></div>`;
        const result = getMarksInDocumentBody();
        expect(result).toEqual([]);
    });

    it("returns all <mark> elements inside the [data-document-body] container", () => {
        document.body.innerHTML = `
            <div data-document-body>
                <mark id="m1">One</mark>
                <mark id="m2">Two</mark>
                <p>Not a mark</p>
                <mark id="m3">Three</mark>
            </div>
        `;
        const result = getMarksInDocumentBody();
        expect(result).toHaveLength(3);
        expect(result.map((m) => m.id)).toEqual(["m1", "m2", "m3"]);
    });
});
