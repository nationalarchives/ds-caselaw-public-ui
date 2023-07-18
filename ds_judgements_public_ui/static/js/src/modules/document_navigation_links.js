import $ from "jquery";

const handler = (entries) => {
    manageClass(entries.some((elem) => elem.isIntersecting));
};

const createObserver = (elements) => {
    const options = { root: null, rootMargin: "0px" };
    const observer = new IntersectionObserver(handler, options);
    elements.forEach((element) => {
        observer.observe(element);
    });
};

const manageClass = (intersecting) => {
    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end",
    );
    const pageScrolls = $(".document-body").height() > $(window).height();

    if (intersecting && pageScrolls) {
        backToTopLinkContainer.classList.remove("show");
    } else if (pageScrolls) {
        backToTopLinkContainer.classList.add("show");
    }
};

$(() => {
    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end",
    );

    let skipToEndLinkContainer = document.getElementById(
        "js-document-navigation-links-start",
    );

    let footerBackLink = document.querySelector(
        ".document-end-document-marker__top-link a",
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
    let judgmentsFooter = document.querySelector(".documents-footer");
    let judgmentsToolbarContainer = document.querySelector(
        ".document-toolbar__container",
    );
    if (judgmentsFooter && judgmentsToolbarContainer) {
        createObserver([judgmentsFooter, judgmentsToolbarContainer]);
    }
});
