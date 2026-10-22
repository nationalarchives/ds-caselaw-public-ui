export function getQueryFromUrl(param = "query"): string {
  const params = new URLSearchParams(window.location.search);
  return params.get(param) || "";
}

export function getMarksInDocumentBody(): HTMLElement[] {
  const bodyContainer = document.querySelector("[data-document-body]");
  if (!bodyContainer) return [];
  return Array.from(bodyContainer.querySelectorAll("mark"));
}
