import $ from "jquery";

const handler = (entries) => {
    manageClass(entries[0].isIntersecting);
};

const createObserver = (element) => {
    const options = { root: null, rootMargin: "0px" };
    const observer = new IntersectionObserver(handler, options);
    observer.observe(element);
};

const manageClass = (intersecting) => {
    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end"
    );
    const pageScrolls = $(".judgment-body").height() > $(window).height();

    if (intersecting && pageScrolls) {
        backToTopLinkContainer.classList.remove("show");
    } else {
        backToTopLinkContainer.classList.add("show");
    }
};

$(() => {
    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end"
    );

    let skipToEndLinkContainer = document.getElementById(
        "js-document-navigation-links-start"
    );

    let footerBackLink = document.querySelector(
        ".end-document-marker__top-link a"
    );

    if (footerBackLink) {
        footerBackLink.classList.add("with-js");
    }

    if (backToTopLinkContainer) {
        backToTopLinkContainer.classList.add("autohide");
        if (skipToEndLinkContainer) {
            $(skipToEndLinkContainer)
                .children()
                .each((_index, link) => {
                    backToTopLinkContainer.appendChild(link);
                });
        }
    }

    createObserver(document.querySelector(".judgments-footer"));
    createObserver(document.querySelector(".judgment-toolbar__container"));
});
