
            document.addEventListener('DOMContentLoaded', function () {
                const dropdownItems = document.querySelectorAll('.dropdown-item[data-color]');
                const themeItems = document.querySelectorAll('.dropdown-item[data-theme]');
                const body = document.getElementById('body');

                dropdownItems.forEach(item => {
                    item.addEventListener('click', function (event) {
                        event.preventDefault();
                        const color = this.getAttribute('data-color');
                        body.style.backgroundColor = color;
                    });
                });

                themeItems.forEach(item => {
                    item.addEventListener('click', function (event) {
                        event.preventDefault();
                        const theme = this.getAttribute('data-theme');
                        if (theme === 'dark') {
                            body.classList.add('dark-theme');
                            body.classList.remove('light-theme');
                        } else {
                            body.classList.add('light-theme');
                            body.classList.remove('dark-theme');
                        }
                    });
                });
            });