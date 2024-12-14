// Appliquer immédiatement le mode sombre si activé dans localStorage
const isDarkMode = localStorage.getItem('dark-mode') === 'enabled';
if (isDarkMode) {
    document.documentElement.classList.add('dark-mode'); // Applique immédiatement la classe au <html>
}

// Attendre que le DOM soit chargé pour ajouter les événements
document.addEventListener('DOMContentLoaded', function () {
    // Récupérer les éléments pertinents
    const body = document.documentElement;
    const modeElements = document.querySelectorAll('.mode');
    const modeToggle = document.querySelector('#mode-toggle');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Charger le mode depuis localStorage (déjà appliqué avant le DOMContentLoaded)
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
