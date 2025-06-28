document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const navbar = document.querySelector('.navbar');
    const themeToggles = document.querySelectorAll('.theme-toggle');
    const themeIcons = document.querySelectorAll('.theme-icon');

    if (!body || !navbar || themeToggles.length === 0 || themeIcons.length === 0) {
        console.warn('Required elements for theme toggle are missing.');
        return;
    }

    // Fonction pour mettre à jour l'icône et le texte
    function updateThemeUI(isDarkMode) {
        themeIcons.forEach(icon => {
            icon.classList.remove('bi-sun', 'bi-moon');
            icon.classList.add(isDarkMode ? 'bi-moon' : 'bi-sun');
        });
    }

    // Appliquer le thème selon localStorage
    function applyTheme(isDarkMode) {
        if (isDarkMode) {
            body.classList.add('dark-mode');
            navbar.classList.add('dark-mode');
            document.querySelectorAll('.card').forEach(el => el.classList.add('dark-mode'));
            document.querySelectorAll('.mode').forEach(el => el.classList.add('dark-mode'));
            document.querySelector('.table')?.classList.add('table-dark');
        } else {
            body.classList.remove('dark-mode');
            navbar.classList.remove('dark-mode');
            document.querySelectorAll('.card').forEach(el => el.classList.remove('dark-mode'));
            document.querySelectorAll('.mode').forEach(el => el.classList.remove('dark-mode'));
            document.querySelector('.table')?.classList.remove('table-dark');
        }
        updateThemeUI(isDarkMode);
    }

    // Initialisation
    let isDarkMode = localStorage.getItem('darkMode') === 'isDarkMode';
    applyTheme(isDarkMode);

    // Toggle au clic
    themeToggles.forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            isDarkMode = !isDarkMode;
            localStorage.setItem('darkMode', isDarkMode ? 'isDarkMode' : 'notDarkMode');
            applyTheme(isDarkMode);
        });
    });
});
