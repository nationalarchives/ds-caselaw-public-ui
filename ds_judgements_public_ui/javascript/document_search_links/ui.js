const HIDE_MATCHES_CLASS = "document-navigation-links--hide-matches";

function createWrapper(className) {
    const span = document.createElement("span");
    span.className = className;
    return span;
}

function createNavLink({ className, title, text }) {
    const link = document.createElement("a");
    link.href = "#";
    link.className = className;
    link.title = title;
    link.textContent = text;
    return link;
}

function setHidden(elements, isHidden) {
    elements.forEach((element) => {
        if (element) {
            element.hidden = isHidden;
        }
    });
}

function createHighlightsToggleLink(elementsToToggle) {
    const link = createNavLink({
        className: "document-navigation-links__highlights-toggle",
        title: "Hide highlights",
        text: "Hide highlights",
    });

    link.addEventListener("click", (event) => {
        event.preventDefault();

        const highlightsAreHidden =
            document.body.classList.toggle(HIDE_MATCHES_CLASS);

        setHidden(elementsToToggle, highlightsAreHidden);

        link.textContent = highlightsAreHidden
            ? "Show highlights"
            : "Hide highlights";

        link.title = highlightsAreHidden
            ? "Show highlights"
            : "Hide highlights";
    });

    return link;
}

function createQueryLabel(queryText) {
    const container = createWrapper(
        "document-navigation-links__search-query-text-container document-navigation-links__query",
    );

    const labelNode = document.createTextNode("Query: ");

    const queryTextSpan = document.createElement("span");
    queryTextSpan.className = "document-navigation-links__query-text";
    queryTextSpan.textContent = queryText;

    container.appendChild(labelNode);
    container.appendChild(queryTextSpan);

    return container;
}

function createMatchCountWrapper(totalMatches, elementsToToggle) {
    const wrapper = createWrapper(
        "document-navigation-links__match-count-wrapper document-navigation-links__matches",
    );

    const matchCountContent = createWrapper(
        "document-navigation-links__match-count-content",
    );

    const positionSpan = document.createElement("span");
    positionSpan.className =
        "document-navigation-links__match-position position";

    const ofText = document.createTextNode(" / ");

    const countSpan = document.createElement("span");
    countSpan.className =
        "document-navigation-links__match-count document-navigation-links__link-count";
    countSpan.textContent = String(totalMatches);

    const separatorText = document.createTextNode(" ");

    matchCountContent.appendChild(positionSpan);
    matchCountContent.appendChild(ofText);
    matchCountContent.appendChild(countSpan);
    matchCountContent.appendChild(separatorText);

    elementsToToggle.push(matchCountContent);

    wrapper.appendChild(matchCountContent);
    wrapper.appendChild(createHighlightsToggleLink(elementsToToggle));

    return wrapper;
}

function createQueryWrapper(queryText, totalMatches, elementsToToggle) {
    const wrapper = createWrapper("document-navigation-links__query-wrapper");

    if (queryText) {
        const queryLabel = createQueryLabel(queryText);
        elementsToToggle.push(queryLabel);
        wrapper.appendChild(queryLabel);
    }

    wrapper.appendChild(
        createMatchCountWrapper(totalMatches, elementsToToggle),
    );

    return wrapper;
}

export function createUI(linksEndContainer, totalMatches, queryText) {
    if (!linksEndContainer) return null;

    if (queryText) {
        linksEndContainer.classList.add("with-query");
    }

    const elementsToToggle = [];

    const leftWrapper = createWrapper(
        "document-navigation-links__left-wrapper",
    );
    const prevLink = createNavLink({
        className: "document-navigation-links__link-left",
        title: "Previous match",
        text: "Previous",
    });
    elementsToToggle.push(prevLink);
    leftWrapper.appendChild(prevLink);

    const rightWrapper = createWrapper(
        "document-navigation-links__right-wrapper",
    );
    const nextLink = createNavLink({
        className: "document-navigation-links__link-right",
        title: "Next match",
        text: "Next",
    });
    elementsToToggle.push(nextLink);
    rightWrapper.appendChild(nextLink);

    const queryWrapper = createQueryWrapper(
        queryText,
        totalMatches,
        elementsToToggle,
    );

    linksEndContainer.appendChild(leftWrapper);
    linksEndContainer.appendChild(queryWrapper);
    linksEndContainer.appendChild(rightWrapper);

    const positionSpan = queryWrapper.querySelector(
        ".document-navigation-links__match-position",
    );

    return {
        prevLink,
        nextLink,
        positionSpan,
    };
}
