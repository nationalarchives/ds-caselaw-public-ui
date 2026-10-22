export interface NavigationOptions {
  smooth?: boolean;
  fromScroll?: boolean;
}

export interface NavigationState {
  getCurrentIndex(): number;
  setCurrent(index: number, options?: NavigationOptions): void;
  next(): void;
  prev(): void;
  updateHighlight(): void;
}

function wrapIndex(index: number, length: number): number {
  return ((index % length) + length) % length;
}

export function createState(
  marks: HTMLElement[],
  positionSpan: HTMLSpanElement,
): NavigationState | null {
  if (!marks.length) return null;

  let currentIndex = 0;

  function updateHighlight() {
    marks.forEach((mark) => mark.classList.remove("current"));
    marks[currentIndex].classList.add("current");
    positionSpan.textContent = String(currentIndex + 1);
  }

  function scrollToCurrent({ smooth } = { smooth: true }) {
    marks[currentIndex].scrollIntoView({
      behavior: smooth ? "smooth" : "auto",
      block: "center",
    });
  }

  function setCurrent(
    index: number,
    { smooth = true, fromScroll = false }: NavigationOptions = {},
  ) {
    currentIndex = wrapIndex(index, marks.length);
    updateHighlight();
    if (!fromScroll) {
      scrollToCurrent({ smooth });
    }
  }

  updateHighlight();

  return {
    getCurrentIndex: () => currentIndex,
    setCurrent,
    next: () => setCurrent(currentIndex + 1),
    prev: () => setCurrent(currentIndex - 1),
    updateHighlight,
  };
}
