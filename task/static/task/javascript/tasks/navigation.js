document.addEventListener('DOMContentLoaded', function () {

setupNavigation();

})

function setupNavigation() {
    const navLinks = document.querySelectorAll('.n');
    const currentUrl = window.location.href;

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add('ac');
        }

        link.addEventListener('click', function () {
            this.classList.add('ac');
        });
    });
}