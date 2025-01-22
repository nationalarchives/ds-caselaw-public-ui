const setupGovukTabsExtended = function () {
    document.querySelectorAll("a[href^='#']").forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");
            const targetElement = document.querySelector(targetId);
            const panelElement = targetElement.closest("[role='tabpanel']");
            const tabElementId = panelElement.getAttribute("aria-labelledby");
            const tab = document.querySelector(`#${tabElementId}`);

            tab.click();
        });
    });
};

document.addEventListener("DOMContentLoaded", setupGovukTabsExtended);
