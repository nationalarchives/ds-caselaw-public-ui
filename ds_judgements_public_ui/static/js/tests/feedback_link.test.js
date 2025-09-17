import {
    describe,
    expect,
    it,
    jest,
    beforeEach,
    afterEach,
} from "@jest/globals";
import { setupFeedbackLink } from "../src/feedback_link";

describe("setupFeedbackLink", () => {
    const setUAData = (data) => {
        Object.defineProperty(navigator, "userAgentData", {
            value: data,
            configurable: true,
        });
    };

    const setPlatform = (platform) => {
        Object.defineProperty(navigator, "platform", {
            value: platform,
            configurable: true,
        });
    };

    const setWindowSize = ({ innerWidth, innerHeight }) => {
        Object.defineProperty(window, "innerWidth", {
            value: innerWidth,
            configurable: true,
        });

        Object.defineProperty(window, "innerHeight", {
            value: innerHeight,
            configurable: true,
        });
    };

    const setClientSize = ({ clientWidth, clientHeight }) => {
        Object.defineProperty(document.documentElement, "clientWidth", {
            value: clientWidth,
            configurable: true,
        });

        Object.defineProperty(document.documentElement, "clientHeight", {
            value: clientHeight,
            configurable: true,
        });
    };

    const resetDOM = (href = "https://example.com/feedback") => {
        document.body.innerHTML = `<a data-feedback-link href="${href}">Feedback</a>`;
    };

    const getParams = () =>
        new URL(document.querySelector("[data-feedback-link]").href)
            .searchParams;

    const saveOriginals = () => ({
        uaData: Object.getOwnPropertyDescriptor(navigator, "userAgentData"),
        platform: Object.getOwnPropertyDescriptor(navigator, "platform"),
        innerWidth: Object.getOwnPropertyDescriptor(window, "innerWidth"),
        innerHeight: Object.getOwnPropertyDescriptor(window, "innerHeight"),
        clientWidth: Object.getOwnPropertyDescriptor(
            document.documentElement,
            "clientWidth",
        ),
        clientHeight: Object.getOwnPropertyDescriptor(
            document.documentElement,
            "clientHeight",
        ),
    });

    let originals;

    beforeEach(() => {
        originals = saveOriginals();
        setUAData(undefined);
        setPlatform("");
        setWindowSize({ innerWidth: 1200, innerHeight: 800 });
        setClientSize({ clientWidth: 1200, clientHeight: 800 });
        resetDOM();
    });

    afterEach(() => {
        const restore = (obj, key, desc) => {
            if (desc) Object.defineProperty(obj, key, desc);
            else delete obj[key];
        };

        restore(navigator, "userAgentData", originals.uaData);
        restore(navigator, "platform", originals.platform);
        restore(window, "innerWidth", originals.innerWidth);
        restore(window, "innerHeight", originals.innerHeight);
        restore(document.documentElement, "clientWidth", originals.clientWidth);
        restore(
            document.documentElement,
            "clientHeight",
            originals.clientHeight,
        );
        document.body.innerHTML = "";
    });

    it("does nothing when no [data-feedback-link] element is present", () => {
        document.body.innerHTML = "";
        expect(() => setupFeedbackLink()).not.toThrow();
    });

    it("uses navigator.userAgentData when available", () => {
        setUAData({ platform: "Windows", mobile: false });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("device-platform")).toBe("Windows");
        expect(params.get("device-class")).toBe("desktop");
        expect(params.get("browser-width")).toBe("1200");
        expect(params.get("browser-height")).toBe("800");
    });

    it("sets device-class to mobile when navigator.userAgentData says mobile", () => {
        setUAData({ platform: "Android", mobile: true });
        setWindowSize({ innerWidth: 1600, innerHeight: 900 });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("device-platform")).toBe("Android");
        expect(params.get("device-class")).toBe("mobile");
    });

    it("falls back to navigator.platform and width breakpoints (<=768 mobile)", () => {
        setUAData(undefined);
        setPlatform("MacIntel");
        setWindowSize({ innerWidth: 768, innerHeight: 700 });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("device-platform")).toBe("MacIntel");
        expect(params.get("device-class")).toBe("mobile");
    });

    it("falls back to width breakpoint for tablet (<=1024)", () => {
        setUAData(undefined);
        setPlatform("Linux x86_64");
        setWindowSize({ innerWidth: 1024, innerHeight: 700 });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("device-platform")).toBe("Linux x86_64");
        expect(params.get("device-class")).toBe("tablet");
    });

    it("falls back to width breakpoint for desktop (>1024)", () => {
        setUAData(undefined);
        setPlatform("Win32");
        setWindowSize({ innerWidth: 1025, innerHeight: 700 });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("device-platform")).toBe("Win32");
        expect(params.get("device-class")).toBe("desktop");
    });

    it("preserves existing query parameters on the link", () => {
        resetDOM("https://example.com/feedback?foo=bar");
        setUAData({ platform: "Windows", mobile: false });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("foo")).toBe("bar");
    });

    it("uses documentElement.clientWidth/Height when window.innerWidth/Height are unavailable", () => {
        setWindowSize({ innerWidth: undefined, innerHeight: undefined });
        setClientSize({ clientWidth: 1111, clientHeight: 777 });
        setUAData({ platform: "Windows", mobile: false });
        setupFeedbackLink();
        const params = getParams();
        expect(params.get("browser-width")).toBe("1111");
        expect(params.get("browser-height")).toBe("777");
    });

    it("does not set device-platform in fallback when navigator.platform is empty", () => {
        setUAData(undefined);
        setPlatform("");
        setWindowSize({ innerWidth: 600, innerHeight: 700 });
        setupFeedbackLink();
        const params = getParams();
        expect(params.has("device-platform")).toBe(false);
        expect(params.get("device-class")).toBe("mobile");
    });
});
