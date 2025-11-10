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

function createMatchCountWrapper(totalMatches) {
    const wrapper = createWrapper(
        "document-navigation-links__match-count-wrapper document-navigation-links__matches",
    );

    const openParen = document.createTextNode(" (");

    const positionSpan = document.createElement("span");
    positionSpan.className =
        "document-navigation-links__match-position position";

    const ofText = document.createTextNode(" of ");

    const countSpan = document.createElement("span");
    countSpan.className =
        "document-navigation-links__match-count document-navigation-links__link-count";
    countSpan.textContent = String(totalMatches);

    const matchesText = document.createTextNode(" matches)");

    wrapper.appendChild(openParen);
    wrapper.appendChild(positionSpan);
    wrapper.appendChild(ofText);
    wrapper.appendChild(countSpan);
    wrapper.appendChild(matchesText);

    return wrapper;
}

function createQueryWrapper(queryText, totalMatches) {
    const wrapper = createWrapper("document-navigation-links__query-wrapper");

    if (queryText) {
        wrapper.appendChild(createQueryLabel(queryText));
    }

    wrapper.appendChild(createMatchCountWrapper(totalMatches));

    return wrapper;
}

export function createUI(linksEndContainer, totalMatches, queryText) {
    if (!linksEndContainer) return null;

    if (queryText) {
        linksEndContainer.classList.add("with-query");
    }

    const leftWrapper = createWrapper(
        "document-navigation-links__left-wrapper",
    );
    const prevLink = createNavLink({
        className: "document-navigation-links__link-left",
        title: "Previous match",
        text: "Previous",
    });
    leftWrapper.appendChild(prevLink);

    const queryWrapper = createQueryWrapper(queryText, totalMatches);

    const rightWrapper = createWrapper(
        "document-navigation-links__right-wrapper",
    );
    const nextLink = createNavLink({
        className: "document-navigation-links__link-right",
        title: "Next match",
        text: "Next",
    });
    rightWrapper.appendChild(nextLink);

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
