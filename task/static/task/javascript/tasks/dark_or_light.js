// Apply dark mode if it's activate in localStorage
const isDarkMode = localStorage.getItem('dark-mode') === 'enabled';
if (isDarkMode) {
    document.documentElement.classList.add('dark-mode'); 
}

document.addEventListener('DOMContentLoaded', function () {

    // variables
    const body = document.documentElement;
    const modeElements = document.querySelectorAll('.mode');
    const modeToggle = document.querySelector('#mode-toggle');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (isDarkMode) {
        enableDarkMode();
    }

    // Ajouter l'événement de basculement du mode
    modeToggle.addEventListener('click', toggleDarkMode);

    // Fonction pour activer le mode sombre
    function enableDarkMode() {
        body.classList.add('dark-mode');
        modeElements.forEach(mode => mode.classList.add('dark-mode'));
        dropdowns.forEach( dropdown => dropdown.setAttribute('data-bs-theme', 'dark'))
        localStorage.setItem('dark-mode', 'enabled');
    }

    // Fonction pour désactiver le mode sombre
    function disableDarkMode() {
        body.classList.remove('dark-mode');
        modeElements.forEach(mode => mode.classList.remove('dark-mode'));
        dropdowns.forEach( dropdown => dropdown.setAttribute('data-bs-theme', 'light'))
        localStorage.setItem('dark-mode', 'disabled');
    }

    // Fonction de basculement entre les modes
    function toggleDarkMode() {
        if (body.classList.contains('dark-mode')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    }
});
