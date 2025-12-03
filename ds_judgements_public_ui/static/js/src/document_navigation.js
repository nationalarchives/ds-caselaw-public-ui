document.addEventListener("DOMContentLoaded", () => {
    const navigation = document.getElementById("js-document-navigation");
    const startSentinel = document.querySelector(
        "[data-document-navigation-start]",
    );
    const endSentinel = document.querySelector(
        "[data-document-navigation-end]",
    );
    const documentBody = document.querySelector("[data-document-body]");

    if (!navigation || !startSentinel || !endSentinel || !documentBody) return;

    navigation.classList.add("autohide");

    const pageScrolls = documentBody.scrollHeight > window.innerHeight;

    const manageClass = (intersecting) => {
        if (!pageScrolls) return;

        if (intersecting) {
            navigation.classList.remove("show");
        } else {
            navigation.classList.add("show");
        }
    };

    const intersectionHandler = (entries) => {
        const isAnyIntersecting = entries.some((entry) => entry.isIntersecting);
        manageClass(isAnyIntersecting);
    };

    const observer = new IntersectionObserver(intersectionHandler, {
        root: null,
        rootMargin: "0px",
    });

    observer.observe(startSentinel);
    observer.observe(endSentinel);
});
