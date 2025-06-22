document.addEventListener('DOMContentLoaded', function () {
    const body = document.getElementById('body');
    const navbar = document.querySelector('.navbar');
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    if (!body || !navbar || !themeToggle || !themeIcon) {
        console.warn('Required elements for theme toggle are missing.');
        return;
    }

    // Fonction pour mettre à jour l'icône et le texte
    function updateThemeUI(isDarkMode) {
        themeIcon.classList.remove('bi-sun', 'bi-moon');
        themeIcon.classList.add(isDarkMode ? 'bi-moon' : 'bi-sun');
        themeToggle.innerHTML = `<i id="theme-icon" class="${isDarkMode ? 'bi-moon' : 'bi-sun'}"></i>   `;
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
    themeToggle.addEventListener('click', function (e) {
        e.preventDefault();
        isDarkMode = !isDarkMode;
        localStorage.setItem('darkMode', isDarkMode ? 'isDarkMode' : 'notDarkMode');
        applyTheme(isDarkMode);
    });
});
