function wrapIndex(index, length) {
    return ((index % length) + length) % length;
}

export function createState(marks, positionSpan) {
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

    function setCurrent(index, { smooth = true, fromScroll = false } = {}) {
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
