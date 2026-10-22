const HIDE_MATCHES_CLASS = "document-navigation-links--hide-matches";

export interface SearchLinksUI {
  prevLink: HTMLAnchorElement;
  nextLink: HTMLAnchorElement;
  positionSpan: HTMLSpanElement;
}

interface NavLinkOptions {
  className: string;
  title: string;
  text: string;
}

function createWrapper(className: string) {
  const span = document.createElement("span");
  span.className = className;
  return span;
}

function createNavLink({ className, title, text }: NavLinkOptions) {
  const link = document.createElement("a");
  link.href = "#";
  link.className = className;
  link.title = title;
  link.textContent = text;
  return link;
}

function setHidden(elements: HTMLElement[], isHidden: boolean) {
  elements.forEach((element) => {
    if (element) {
      element.hidden = isHidden;
    }
  });
}

function createHighlightsToggleLink(elementsToToggle: HTMLElement[]) {
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

    link.title = highlightsAreHidden ? "Show highlights" : "Hide highlights";
  });

  return link;
}

function createQueryLabel(queryText: string) {
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

function createMatchCountWrapper(
  totalMatches: number,
  elementsToToggle: HTMLElement[],
) {
  const wrapper = createWrapper(
    "document-navigation-links__match-count-wrapper document-navigation-links__matches",
  );

  const matchCountContent = createWrapper(
    "document-navigation-links__match-count-content",
  );

  const positionSpan = document.createElement("span");
  positionSpan.className = "document-navigation-links__match-position position";

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

function createQueryWrapper(
  queryText: string,
  totalMatches: number,
  elementsToToggle: HTMLElement[],
) {
  const wrapper = createWrapper("document-navigation-links__query-wrapper");

  if (queryText) {
    const queryLabel = createQueryLabel(queryText);
    elementsToToggle.push(queryLabel);
    wrapper.appendChild(queryLabel);
  }

  wrapper.appendChild(createMatchCountWrapper(totalMatches, elementsToToggle));

  return wrapper;
}

export function createUI(
  linksEndContainer: HTMLElement | null,
  totalMatches: number,
  queryText: string,
): SearchLinksUI | null {
  if (!linksEndContainer) return null;

  if (queryText) {
    linksEndContainer.classList.add("with-query");
  }

  const elementsToToggle: HTMLElement[] = [];

  const leftWrapper = createWrapper("document-navigation-links__left-wrapper");
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

  const positionSpan = queryWrapper.querySelector<HTMLSpanElement>(
    ".document-navigation-links__match-position",
  );
  if (!positionSpan) return null;

  return {
    prevLink,
    nextLink,
    positionSpan,
  };
}
