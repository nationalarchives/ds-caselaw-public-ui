export function attachMarkScrollSync(marks, navState) {
    if (!marks.length || !navState) return;

    const observer = new IntersectionObserver(
        (entries) => {
            const visible = entries.filter((entry) => entry.isIntersecting);
            if (!visible.length) return;

            const last = visible[visible.length - 1];
            const index = marks.indexOf(last.target);
            if (index !== -1 && index !== navState.getCurrentIndex()) {
                navState.setCurrent(index, { smooth: false, fromScroll: true });
            }
        },
        {
            root: null,
            rootMargin: "-25% 0px -25% 0px",
        },
    );

    marks.forEach((mark) => observer.observe(mark));
}
