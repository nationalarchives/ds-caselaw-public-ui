import {
  describe,
  expect,
  it,
  beforeEach,
  afterEach,
  jest,
} from "@jest/globals";
import { attachMarkScrollSync } from "./scrolling";
import type { ScrollNavigationState } from "./scrolling";

describe("attachMarkScrollSync", () => {
  const originalObserver = window.IntersectionObserver;
  let observeMock: ReturnType<typeof jest.fn<IntersectionObserver["observe"]>>;
  let disconnectMock: ReturnType<
    typeof jest.fn<IntersectionObserver["disconnect"]>
  >;
  let observerCallback: IntersectionObserverCallback;
  let observer: IntersectionObserver;
  let navState: jest.Mocked<ScrollNavigationState>;
  const observerConstructor =
    jest.fn<(options?: IntersectionObserverInit) => void>();

  function intersectionObserverCallback(
    entries: Pick<IntersectionObserverEntry, "target" | "isIntersecting">[],
  ) {
    observerCallback(
      entries.map((entry) => ({
        ...entry,
        boundingClientRect: entry.target.getBoundingClientRect(),
        intersectionRect: entry.target.getBoundingClientRect(),
        rootBounds: null,
        intersectionRatio: entry.isIntersecting ? 1 : 0,
        time: 0,
      })),
      observer,
    );
  }

  afterEach(() => {
    window.IntersectionObserver = originalObserver;
  });

  beforeEach(() => {
    document.body.innerHTML = "";

    observeMock = jest.fn<IntersectionObserver["observe"]>();
    disconnectMock = jest.fn<IntersectionObserver["disconnect"]>();
    observerConstructor.mockClear();

    window.IntersectionObserver = class implements IntersectionObserver {
      readonly root = null;
      readonly rootMargin = "-25% 0px -25% 0px";
      readonly scrollMargin = "0px";
      readonly thresholds = [0];
      observe = observeMock;
      unobserve = jest.fn<IntersectionObserver["unobserve"]>();
      disconnect = disconnectMock;
      takeRecords = jest
        .fn<IntersectionObserver["takeRecords"]>()
        .mockReturnValue([]);

      constructor(
        callback: IntersectionObserverCallback,
        options?: IntersectionObserverInit,
      ) {
        observerCallback = callback;
        observer = this;
        observerConstructor(options);
      }
    };

    navState = {
      getCurrentIndex: jest
        .fn<ScrollNavigationState["getCurrentIndex"]>()
        .mockReturnValue(0),
      setCurrent: jest.fn<ScrollNavigationState["setCurrent"]>(),
    };
  });

  it("does nothing if marks array is empty", () => {
    attachMarkScrollSync([], navState);

    expect(observerConstructor).not.toHaveBeenCalled();
    expect(navState.setCurrent).not.toHaveBeenCalled();
  });

  it("does nothing if navState is falsy", () => {
    const mark = document.createElement("div");

    attachMarkScrollSync([mark], null);

    expect(observerConstructor).not.toHaveBeenCalled();
  });

  it("creates an IntersectionObserver with the correct options and observes all marks", () => {
    const mark1 = document.createElement("div");
    const mark2 = document.createElement("div");
    const mark3 = document.createElement("div");

    attachMarkScrollSync([mark1, mark2, mark3], navState);

    expect(observerConstructor).toHaveBeenCalledTimes(1);

    const [options] = observerConstructor.mock.calls[0];
    expect(options).toEqual({
      root: null,
      rootMargin: "-25% 0px -25% 0px",
    });

    expect(observeMock).toHaveBeenCalledTimes(3);
    expect(observeMock.mock.calls[0][0]).toBe(mark1);
    expect(observeMock.mock.calls[1][0]).toBe(mark2);
    expect(observeMock.mock.calls[2][0]).toBe(mark3);
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

    intersectionObserverCallback([{ target: mark1, isIntersecting: false }]);

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
