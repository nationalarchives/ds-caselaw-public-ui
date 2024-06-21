function highlightCurrentPage() {
    const currentPageUrl = window.location.pathname;
    const menuItem = document.querySelector(
        '.govuk-header__navigation-item a[href="' + currentPageUrl + '"]',
    );
    console.log(menuItem);
    if (menuItem) {
        menuItem.classList.add("active");
    }
}
document.addEventListener("DOMContentLoaded", highlightCurrentPage);
