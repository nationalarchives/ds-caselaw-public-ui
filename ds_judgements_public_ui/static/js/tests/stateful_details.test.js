import { describe, expect, it, jest } from "@jest/globals";
import { getCookie, initStatefulDetails } from "../src/stateful_details";

describe("getCookie", () => {
    it("returns null when the cookie string is empty", () => {
        expect(getCookie("a", "")).toBe(null);
        expect(getCookie("a", null)).toBe(null);
    });

    it("returns the decoded value for an existing cookie", () => {
        const cookieString = "a=1; b=hello%20world; c=%7B%22x%22%3A1%7D";
        expect(getCookie("b", cookieString)).toBe("hello world");
        expect(getCookie("c", cookieString)).toBe('{"x":1}');
    });

    it("returns an empty string for a cookie with no value", () => {
        expect(getCookie("a", "a=; b=2")).toBe("");
    });

    it("matches a cookie key with URL-encoded characters", () => {
        const cookieString = "dont%20show=true; other=1";
        expect(getCookie("dont show", cookieString)).toBe("true");
    });

    it("returns null when the cookie is not present", () => {
        expect(getCookie("missing", "a=1; b=2")).toBe(null);
    });

    it("handles a cookie token without '=' as an empty value", () => {
        expect(getCookie("flag", "flag; a=1")).toBe("");
    });
});

describe("initStatefulDetails", () => {
    it("returns a no-op cleanup when details is null/undefined", () => {
        const cleanup = initStatefulDetails(null);
        expect(typeof cleanup).toBe("function");
        cleanup();
    });

    it("sets details.open to true when dontShow cookie is not true", () => {
        document.body.innerHTML = `
      <details data-stateful-details>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=false",
        });

        expect(details.open).toBe(true);
    });

    it("sets details.open to false when dontShow cookie is true", () => {
        document.body.innerHTML = `
      <details data-stateful-details>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=true",
        });

        expect(details.open).toBe(false);
    });

    it("initially hides the closed title when present", () => {
        document.body.innerHTML = `
      <details data-stateful-details>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const closedTitle = document.querySelector(
            "[data-stateful-details-close-title]",
        );

        initStatefulDetails(details, { cookieString: "" });

        expect(closedTitle.hidden).toBe(true);
    });

    it("does nothing on toggle until the user has interacted", () => {
        jest.useFakeTimers();

        document.body.innerHTML = `
      <details data-stateful-details>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const summary = details.querySelector("summary");
        const closedTitle = details.querySelector(
            "[data-stateful-details-close-title]",
        );

        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=false",
            hideClosedTitleAfterMs: 10,
        });

        details.open = false;
        details.dispatchEvent(new Event("toggle"));

        expect(closedTitle.hidden).toBe(true);
        jest.runOnlyPendingTimers();
        expect(closedTitle.hidden).toBe(true);

        jest.useRealTimers();
    });

    it("when user has interacted, closing details shows closed title then hides it after hideClosedTitleAfterMs", () => {
        jest.useFakeTimers();

        document.body.innerHTML = `
      <details data-stateful-details open>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const summary = details.querySelector("summary");
        const closedTitle = details.querySelector(
            "[data-stateful-details-close-title]",
        );

        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=false",
            hideClosedTitleAfterMs: 50,
        });

        summary.dispatchEvent(new MouseEvent("click", { bubbles: true }));

        details.open = false;
        details.dispatchEvent(new Event("toggle"));

        expect(closedTitle.hidden).toBe(false);

        jest.advanceTimersByTime(49);
        expect(closedTitle.hidden).toBe(false);

        jest.advanceTimersByTime(1);
        expect(closedTitle.hidden).toBe(true);

        jest.useRealTimers();
    });

    it("when user has interacted, opening details hides closed title and clears any hide timer", () => {
        jest.useFakeTimers();

        document.body.innerHTML = `
      <details data-stateful-details open>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const summary = details.querySelector("summary");
        const closedTitle = details.querySelector(
            "[data-stateful-details-close-title]",
        );

        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=false",
            hideClosedTitleAfterMs: 100,
        });

        summary.dispatchEvent(new MouseEvent("click", { bubbles: true }));

        details.open = false;
        details.dispatchEvent(new Event("toggle"));
        expect(closedTitle.hidden).toBe(false);

        details.open = true;
        details.dispatchEvent(new Event("toggle"));
        expect(closedTitle.hidden).toBe(true);

        jest.runOnlyPendingTimers();
        expect(closedTitle.hidden).toBe(true);

        jest.useRealTimers();
    });

    it("does not show the closed title when dontShow cookie is true (even after interaction)", () => {
        jest.useFakeTimers();

        document.body.innerHTML = `
      <details data-stateful-details>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const summary = details.querySelector("summary");
        const closedTitle = details.querySelector(
            "[data-stateful-details-close-title]",
        );

        initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=true",
            hideClosedTitleAfterMs: 10,
        });

        summary.dispatchEvent(new MouseEvent("click", { bubbles: true }));

        details.open = false;
        details.dispatchEvent(new Event("toggle"));

        expect(closedTitle.hidden).toBe(true);

        jest.runOnlyPendingTimers();
        expect(closedTitle.hidden).toBe(true);

        jest.useRealTimers();
    });

    it("cleanup removes event listeners and clears timers", () => {
        jest.useFakeTimers();

        document.body.innerHTML = `
      <details data-stateful-details open>
        <summary>Cookie notice</summary>
        <span data-stateful-details-close-title>Closed</span>
      </details>
    `;

        const details = document.querySelector("[data-stateful-details]");
        const summary = details.querySelector("summary");
        const closedTitle = details.querySelector(
            "[data-stateful-details-close-title]",
        );

        const cleanup = initStatefulDetails(details, {
            cookieString: "dontShowCookieNotice=false",
            hideClosedTitlehideAfterMs: 100,
        });

        summary.dispatchEvent(new MouseEvent("click", { bubbles: true }));

        details.open = false;
        details.dispatchEvent(new Event("toggle"));
        expect(closedTitle.hidden).toBe(false);

        cleanup();

        jest.runOnlyPendingTimers();
        expect(closedTitle.hidden).toBe(false);

        details.open = true;
        details.dispatchEvent(new Event("toggle"));
        expect(closedTitle.hidden).toBe(false);

        jest.useRealTimers();
    });
});
