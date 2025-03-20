import $ from "jquery";

var currentMatch = null;
var totalMatches;
var leftLink;
var rightLink;
var positionContainer;

const modulo = (x, y) => {
    // Javascript doesn't have a real modulo operator. Adapted from:
    // https://web.archive.org/web/20090717035140if_/javascript.about.com/od/problemsolving/a/modulobug.htm
    return ((x % y) + y) % y;
};

const furnitureIntersectionHandler = (entries) => {
    manageClass(entries.some((elem) => elem.isIntersecting));
};

const createIntersectionObserver = (elements, handler, options) => {
    if (options == undefined) {
        options = { root: null, rootMargin: "0px" };
    }
    const observer = new IntersectionObserver(handler, options);
    elements.forEach((element) => {
        observer.observe(element);
    });
};

const manageClass = (intersecting) => {
    const documentNavigationContainer = document.getElementById(
        "js-document-navigation",
    );
    const pageScrolls = $(".judgment-body").height() > $(window).height();

    if (intersecting && pageScrolls) {
        documentNavigationContainer.classList.remove("show");
    } else if (pageScrolls) {
        documentNavigationContainer.classList.add("show");
    }
};

const updateMatchHighlighting = (highlightMatch) => {
    $("mark.current").removeClass("current");
    if (currentMatch != null && highlightMatch) {
        $(`#mark_${currentMatch}`).addClass("current");
    }
};

const updateMatchPositionLabel = () => {
    if (positionContainer) {
        if (currentMatch == null) {
            positionContainer.text(0);
        } else {
            positionContainer.text(currentMatch + 1);
        }
    }
};

const setCurrentMatch = (matchNumber, highlightMatch) => {
    if (highlightMatch == undefined) {
        highlightMatch = true;
    }
    if (matchNumber == null) {
        currentMatch = null;
    } else {
        currentMatch = modulo(matchNumber, totalMatches);
    }
    updateMatchHighlighting(highlightMatch);
    updateMatchPositionLabel();
};

const incrementCurrentMatch = () => {
    if (currentMatch == null) {
        setCurrentMatch(0);
    } else {
        setCurrentMatch(currentMatch + 1);
    }
};

const decrementCurrentMatch = () => {
    if (currentMatch == null) {
        setCurrentMatch(totalMatches - 1);
    } else {
        setCurrentMatch(currentMatch - 1);
    }
};

$(() => {
    const documentNavigationContainer = document.getElementById(
        "js-document-navigation",
    );

    const backToTopLinkContainer = document.getElementById(
        "js-document-navigation-links-end",
    );

    let skipToEndLinkContainer = document.getElementById(
        "js-document-navigation-links-start",
    );

    let footerBackLink = document.querySelector(
        ".judgment-end-document-marker__top-link a",
    );

    if (footerBackLink) {
        footerBackLink.classList.add("with-js");
    }

    if (documentNavigationContainer) {
        documentNavigationContainer.classList.add("autohide");
    }

    if (backToTopLinkContainer) {
        if (skipToEndLinkContainer) {
            skipToEndLinkContainer.classList.add("autohide");
            $(skipToEndLinkContainer)
                .children()
                .each((_index, link) => {
                    backToTopLinkContainer.appendChild(link);
                });
        }
    }

    let queryContainer = document.getElementById(
        "js-document-navigation-links-query-container",
    );

    if (queryContainer) {
        const countContainer = $(queryContainer).find(
            ".document-navigation-links__link-count",
        );
        totalMatches = parseInt(countContainer.text());

        $(queryContainer).before(
            `<span class="document-navigation-links__left-wrapper"><a class="document-navigation-links__link-left" title="Previous match" href="#">Previous</a></span>`,
        );
        $(queryContainer).after(
            `<span class="document-navigation-links__right-wrapper"><a class="document-navigation-links__link-right" href="#" title="Next match">Next</a></span>`,
        );
        positionContainer = $(
            `<span class="document-navigation-links__match-position position">0</span>`,
        );

        positionContainer.insertBefore(countContainer);
        $($.parseHTML(" of ")).insertBefore(countContainer);

        leftLink = $(backToTopLinkContainer).find(
            ".document-navigation-links__link-left",
        );

        if (
            window.location.hash &&
            window.location.hash.match(/^#mark_(\d+)$/)
        ) {
            const match = parseInt(window.location.hash.replace("#mark_", ""));
            setCurrentMatch(match);
        }

        leftLink.on("click", function (event) {
            event.preventDefault();
            decrementCurrentMatch();
            document.getElementById(`mark_${currentMatch}`).scrollIntoView();
        });

        rightLink = $(backToTopLinkContainer).find(
            ".document-navigation-links__right-wrapper",
        );

        rightLink.on("click", function (event) {
            event.preventDefault();
            incrementCurrentMatch();
            document.getElementById(`mark_${currentMatch}`).scrollIntoView();
        });

        createIntersectionObserver(
            $("mark").toArray(),
            (entries) => {
                const entry = entries[entries.length - 1];
                if (entry) {
                    const markNumber = parseInt(
                        entry.target.id.replace("mark_", ""),
                    );
                    if (entry.isIntersecting) {
                        setCurrentMatch(markNumber, true);
                    }
                }
            },
            {
                root: null,
                rootMargin: `-25% 0px -25% 0px`,
            },
        );

        $("#start-of-document-link").text("Top");
        $("#end-of-document-link").text("End");
    }

    $(".document-navigation-link").on("click", (event) => {
        const targetId = $(event.target).attr("href").replace("#", "");
        event.preventDefault();
        setCurrentMatch(null);
        document.getElementById(targetId).scrollIntoView();
    });

    let judgmentsFooter = document.querySelector(".site-footer");
    let judgmentsToolbarContainer = document.querySelector(
        ".judgment-toolbar__container",
    );
    if (judgmentsFooter && judgmentsToolbarContainer) {
        createIntersectionObserver(
            [judgmentsFooter, judgmentsToolbarContainer],
            furnitureIntersectionHandler,
        );
    }
});
