import { describe, expect, it, beforeEach, jest } from "@jest/globals";
import { createState } from "../../src/document_search_links/state";

describe("createState", () => {
    let marks;
    let positionSpan;

    function createMark(id) {
        const el = document.createElement("div");
        el.id = id;
        el.scrollIntoView = jest.fn();
        return el;
    }

    beforeEach(() => {
        document.body.innerHTML = "";
        positionSpan = document.createElement("span");

        marks = [
            createMark("mark-1"),
            createMark("mark-2"),
            createMark("mark-3"),
        ];
    });

    it("returns null when no marks are provided", () => {
        const state = createState([], positionSpan);

        expect(state).toBeNull();
    });

    it("initialises with index 0 highlighted and positionSpan set", () => {
        const state = createState(marks, positionSpan);

        expect(state).not.toBeNull();
        expect(state.getCurrentIndex()).toBe(0);

        expect(marks[0].classList.contains("current")).toBe(true);
        expect(marks[1].classList.contains("current")).toBe(false);
        expect(marks[2].classList.contains("current")).toBe(false);

        expect(positionSpan.textContent).toBe("1");
    });

    it("setCurrent updates current index, highlight, positionSpan and scrolls (default smooth)", () => {
        const state = createState(marks, positionSpan);

        state.setCurrent(1);

        expect(state.getCurrentIndex()).toBe(1);

        expect(marks[0].classList.contains("current")).toBe(false);
        expect(marks[1].classList.contains("current")).toBe(true);
        expect(marks[2].classList.contains("current")).toBe(false);

        expect(positionSpan.textContent).toBe("2");

        expect(marks[1].scrollIntoView).toHaveBeenCalledTimes(1);
        expect(marks[1].scrollIntoView).toHaveBeenCalledWith({
            behavior: "smooth",
            block: "center",
        });
    });

    it("setCurrent respects smooth = false (uses behavior: 'auto')", () => {
        const state = createState(marks, positionSpan);

        state.setCurrent(2, { smooth: false });

        expect(state.getCurrentIndex()).toBe(2);
        expect(positionSpan.textContent).toBe("3");

        expect(marks[2].scrollIntoView).toHaveBeenCalledWith({
            behavior: "auto",
            block: "center",
        });
    });

    it("does not scroll when fromScroll is true, but still updates highlight and index", () => {
        const state = createState(marks, positionSpan);

        state.setCurrent(2, { fromScroll: true });

        expect(state.getCurrentIndex()).toBe(2);
        expect(positionSpan.textContent).toBe("3");

        expect(marks[2].classList.contains("current")).toBe(true);
        expect(marks[2].scrollIntoView).not.toHaveBeenCalled();
    });

    it("next() advances index and wraps around using wrapIndex", () => {
        const state = createState(marks, positionSpan);

        state.next();
        expect(state.getCurrentIndex()).toBe(1);
        expect(positionSpan.textContent).toBe("2");

        state.next();
        expect(state.getCurrentIndex()).toBe(2);
        expect(positionSpan.textContent).toBe("3");

        state.next();
        expect(state.getCurrentIndex()).toBe(0);
        expect(positionSpan.textContent).toBe("1");
    });

    it("prev() decrements index and wraps around using wrapIndex", () => {
        const state = createState(marks, positionSpan);

        state.prev();
        expect(state.getCurrentIndex()).toBe(2);
        expect(positionSpan.textContent).toBe("3");

        state.prev();
        expect(state.getCurrentIndex()).toBe(1);
        expect(positionSpan.textContent).toBe("2");
    });

    it("updateHighlight only updates classes and positionSpan without re-scrolling", () => {
        const state = createState(marks, positionSpan);

        state.setCurrent(1, { fromScroll: true });
        marks[1].scrollIntoView.mockClear();

        state.updateHighlight();

        expect(marks[0].classList.contains("current")).toBe(false);
        expect(marks[1].classList.contains("current")).toBe(true);
        expect(marks[2].classList.contains("current")).toBe(false);
        expect(positionSpan.textContent).toBe("2");

        expect(marks[1].scrollIntoView).not.toHaveBeenCalled();
    });
});
