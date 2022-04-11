const handler = (entries) => {
    manage_class(entries[0].isIntersecting)
};

const createObserver = (element) => {
    const options = {root: null, rootMargin: "0px"};
    const observer = new IntersectionObserver(handler, options);
    observer.observe(element);
};

const manage_class = (intersecting) => {
    const button = document.getElementById('js-back-to-top-link');

    if (intersecting) {
        button.classList.add('show');
    } else {
        button.classList.remove('show');
    }
};

let judgment_body = document.querySelector('.judgment-body');

if (judgment_body) {
    createObserver(judgment_body);
}
