document.addEventListener('DOMContentLoaded', function(){

    if (localStorage.getItem('darkMode') === 'isDarkMode') {
        document.documentElement.classList.add('dark-mode');
    }
                            const body = document.getElementById('body');
                            const navbar = document.querySelector('.navbar');
                            const lightMode = document.getElementById('light-mode');
                            const darkMode = document.getElementById('dark-mode');
                            const themeIcon = document.getElementById('theme-icon');

                            if (!body || !navbar || !lightMode || !darkMode || !themeIcon) {
                                console.warn('Required elements for theme toggle are missing.');
                                return;
                            }

                            // Function to update the theme icon
                            function updateThemeIcon(isDarkMode) {
                                themeIcon.classList.remove('bi-sun', 'bi-moon');
                                themeIcon.classList.add(isDarkMode ? 'bi-moon' : 'bi-sun');
                            }

                            // Load the theme state from localStorage
                            const darkModeEnabled = localStorage.getItem('darkMode') === 'isDarkMode';
                            if (darkModeEnabled) {
                                body.classList.add('dark-mode');
                                navbar.classList.add('dark-mode');
                                document.querySelectorAll('.card').forEach(element => element.classList.add('dark-mode'));
                                document.querySelectorAll('.mode').forEach(element => element.classList.add('dark-mode'));
                                document.querySelector('.table').classList.add('table-dark');
                                updateThemeIcon(true);
                            } else {
                                updateThemeIcon(false);
                            }

                            lightMode.addEventListener('click', function () {
                                body.classList.remove('dark-mode');
                                navbar.classList.remove('dark-mode');
                                document.querySelectorAll('.card').forEach(element => element.classList.remove('dark-mode'));
                                document.querySelectorAll('.mode').forEach(element => element.classList.remove('dark-mode'));
                                document.querySelector('.table').classList.remove('table-dark');
                                localStorage.setItem('darkMode', 'notDarkMode');
                                updateThemeIcon(false);
                            });

                            darkMode.addEventListener('click', function () {
                                body.classList.add('dark-mode');
                                navbar.classList.add('dark-mode');
                                document.querySelectorAll('.card').forEach(element => element.classList.add('dark-mode'));
                                document.querySelectorAll('.mode').forEach(element => element.classList.add('dark-mode'));
                                document.querySelector('.table').classList.add('table-dark');
                                localStorage.setItem('darkMode', 'isDarkMode');
                                updateThemeIcon(true);
                            });
})