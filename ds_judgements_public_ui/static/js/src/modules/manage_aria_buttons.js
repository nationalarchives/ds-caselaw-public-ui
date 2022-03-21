let btns = document.querySelectorAll('[role=button]');

Array.prototype.forEach.call(btns, function (btn) {
    btn.addEventListener('keydown', event => {
        if (event.key !== 'Enter' && event.key !== ' ') {
            return;
        }
        event.preventDefault(); // Prevent scroll behaviour
        btn.click();
    })
});
