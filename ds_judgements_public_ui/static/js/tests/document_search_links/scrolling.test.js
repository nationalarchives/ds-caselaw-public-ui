import { describe, expect, it, beforeEach, jest } from "@jest/globals";
import { attachMarkScrollSync } from "../../src/document_search_links/scrolling";

describe("attachMarkScrollSync", () => {
    let observeMock;
    let disconnectMock;
    let intersectionObserverCallback;
    let navState;

    beforeEach(() => {
        document.body.innerHTML = "";

        observeMock = jest.fn();
        disconnectMock = jest.fn();
        intersectionObserverCallback = undefined;

        global.IntersectionObserver = jest.fn((callback, options) => {
            intersectionObserverCallback = callback;

            return {
                observe: observeMock,
                unobserve: jest.fn(),
                disconnect: disconnectMock,
                takeRecords: jest.fn(),
            };
        });

        navState = {
            getCurrentIndex: jest.fn().mockReturnValue(0),
            setCurrent: jest.fn(),
        };
    });

    it("does nothing if marks array is empty", () => {
        attachMarkScrollSync([], navState);

        expect(global.IntersectionObserver).not.toHaveBeenCalled();
        expect(navState.setCurrent).not.toHaveBeenCalled();
    });

    it("does nothing if navState is falsy", () => {
        const mark = document.createElement("div");

        attachMarkScrollSync([mark], null);

        expect(global.IntersectionObserver).not.toHaveBeenCalled();
    });

    it("creates an IntersectionObserver with the correct options and observes all marks", () => {
        const mark1 = document.createElement("div");
        const mark2 = document.createElement("div");
        const mark3 = document.createElement("div");

        attachMarkScrollSync([mark1, mark2, mark3], navState);

        expect(global.IntersectionObserver).toHaveBeenCalledTimes(1);

        const [, options] = global.IntersectionObserver.mock.calls[0];
        expect(options).toEqual({
            root: null,
            rootMargin: "-25% 0px -25% 0px",
        });

        expect(observeMock).toHaveBeenCalledTimes(3);
        expect(observeMock).toHaveBeenCalledWith(mark1);
        expect(observeMock).toHaveBeenCalledWith(mark2);
        expect(observeMock).toHaveBeenCalledWith(mark3);
    });

    it("sets current index when an observed mark becomes visible", () => {
        const mark1 = document.createElement("div");
        const mark2 = document.createElement("div");
        const mark3 = document.createElement("div");
        const marks = [mark1, mark2, mark3];

        navState.getCurrentIndex.mockReturnValue(0);

        attachMarkScrollSync(marks, navState);

        intersectionObserverCallback([
            { target: mark1, isIntersecting: true },
            { target: mark2, isIntersecting: true },
        ]);

        expect(navState.setCurrent).toHaveBeenCalledWith(1, {
            smooth: false,
            fromScroll: true,
        });
    });

    it("uses the last visible entry when multiple marks are intersecting", () => {
        const mark1 = document.createElement("div");
        const mark2 = document.createElement("div");
        const mark3 = document.createElement("div");
        const marks = [mark1, mark2, mark3];

        navState.getCurrentIndex.mockReturnValue(0);

        attachMarkScrollSync(marks, navState);

        intersectionObserverCallback([
            { target: mark1, isIntersecting: true },
            { target: mark2, isIntersecting: true },
            { target: mark3, isIntersecting: true },
        ]);

        expect(navState.setCurrent).toHaveBeenCalledWith(2, {
            smooth: false,
            fromScroll: true,
        });
    });

    it("does not call setCurrent if no entries are visible", () => {
        const mark1 = document.createElement("div");
        const marks = [mark1];

        attachMarkScrollSync(marks, navState);

        intersectionObserverCallback([
            { target: mark1, isIntersecting: false },
        ]);

        expect(navState.setCurrent).not.toHaveBeenCalled();
    });

    it("does not call setCurrent if index is -1 (target not in marks)", () => {
        const mark1 = document.createElement("div");
        const marks = [mark1];

        attachMarkScrollSync(marks, navState);

        const notInMarks = document.createElement("div");

        intersectionObserverCallback([
            { target: notInMarks, isIntersecting: true },
        ]);

        expect(navState.setCurrent).not.toHaveBeenCalled();
    });

    it("does not call setCurrent if index is already the current index", () => {
        const mark1 = document.createElement("div");
        const marks = [mark1];

        navState.getCurrentIndex.mockReturnValue(0);

        attachMarkScrollSync(marks, navState);

        intersectionObserverCallback([{ target: mark1, isIntersecting: true }]);

        expect(navState.setCurrent).not.toHaveBeenCalled();
    });
});
