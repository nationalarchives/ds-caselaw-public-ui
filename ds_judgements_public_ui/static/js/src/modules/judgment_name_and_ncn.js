import $ from "jquery";

function clickCopyLink(event) {
    event.preventDefault();
    let str = $(".judgment-name-and-ncn__text")[0];
    window.getSelection().selectAllChildren(str);
    document.execCommand("Copy");
}

function displayCopyLink() {
    $(".judgment-name-and-ncn__copy-link").show();
}

function bindCopyLinkClick() {
    $(".judgment-name-and-ncn__copy-link").on("click", clickCopyLink);
}

$(function () {
    displayCopyLink();
    bindCopyLinkClick();
});
