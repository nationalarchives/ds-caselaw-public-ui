import { CookieBanner } from "@nationalarchives/frontend/nationalarchives/components/cookie-banner/cookie-banner.mjs";
import Cookies from "@nationalarchives/cookies";

document.addEventListener("DOMContentLoaded", () => {
    new Cookies();

    const cookieBannerElement = document.querySelector(
        '[data-module="tna-cookie-banner"]',
    );

    if (cookieBannerElement) {
        new CookieBanner(cookieBannerElement);
    }
});
