document.addEventListener('DOMContentLoaded', function(){

    setupEventHandlers();
    setupTaskCompletionHandler();

})


/**
 * Sets up event handlers for various user interactions on the page.
 */
function setupEventHandlers() {

    document.querySelectorAll('.m').forEach(m => {
        m.addEventListener('click', function () {
            loadTaskDetails(this.dataset.id);
        });
    });

    document.querySelectorAll('.m3').forEach(m3 => {
        m3.addEventListener('click', function(){
            loadNewTask()
        });
    });


    document.querySelectorAll('.m2').forEach(m2 => {
        m2.addEventListener('click', function () {
            loadUpdateTask(this.dataset.id);
        });
    });

    
}

/**
 * Sets up event handlers for marking tasks as completed.
 */
function setupTaskCompletionHandler() {
    document.querySelectorAll('.com').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.dataset.id;
            fetch(`/task/${id}`, {
                method: 'PUT',
                body: JSON.stringify({ completed: true })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);

                })
                .catch(error => console.error('Error:', error))

            location.reload();

        });
    });
}


/**
 * Updates icons for navigation elements based on the active ID.
 */
function updateIcons(activeId) {
    document.querySelectorAll('.v').forEach(v => {
        let icon = v.querySelector('.bi');

        if (!icon) {
            icon = document.createElement('i');
            icon.className = 'bi bi-toggle-on toggle'; // Bootstrap Icon class
        }

        if (v.dataset.id === activeId) {
            if (!v.contains(icon)) v.prepend(icon);
        } else {
            if (v.contains(icon)) icon.remove();
        }
    });
}



/**
 * Fetches and displays the form to update an existing task in a modal.
 */
function loadUpdateTask(taskId) {
    fetch(`/update_task/${taskId}`)
        .then(response => response.text())
        .then(data => {
            displayModal(data)
            const dateInput = document.querySelector('#due_date');
            const calendarButton = document.querySelector('#calendar-button')

            flatpickr(dateInput, {
                dateFormat: "Y-m-d", // Format de la date
                minDate: "today",    // Dates à partir d'aujourd'hui
                altInput: true,      // Ajoute un champ stylisé
                weekNumbers: true,
            });
            calendarButton.addEventListener('click', function () {
                dateInput._flatpickr.open();
            });


        })
        .catch(error => console.error('Error fetching update task:', error));
}


/**
 * Fetches and displays task details in a modal.
 */
function loadTaskDetails(taskId) {
    fetch(`/task_detail/${taskId}`)
        .then(response => response.text())
        .then(data => {
            displayModal(data);
            const updateButton = document.querySelector('.m2');
            if (updateButton) {  // Vérifiez que le bouton existe avant d'ajouter un écouteur
                updateButton.removeEventListener('click', handleUpdateTask);  // Supprimez tout ancien écouteur
                updateButton.addEventListener('click', handleUpdateTask);  // Ajoutez un nouvel écouteur
            }
            function handleUpdateTask() {
                loadUpdateTask(taskId);
            }
            document.querySelector('#com').addEventListener('click', function(){
                console.log('1')
                const id = this.dataset.id;
                fetch(`/task/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({ completed: true })
                })
                .then( response => response.json() )
                .then(data => {
                    console.log(data)
                } )
            });
            })
}

/**
 * Updates a task with the form data and reloads the task details.
 */
function updateTask(taskId) {
    const title = document.querySelector('#task-title').value;
    const description = document.querySelector('#task-description').value;
    const dueDate = document.querySelector('#task-due-date').value;
    const priority = document.querySelector('#task-priority').value;
    const category = document.querySelector('#task-category').value;

    const requestData = { title, description, dueDate, priority, category };
    console.log('Sending request with data:', requestData);

    fetch(`/update_task/${taskId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
    })
        .then(function () {
            sendNotification("Your task is Updated", `Votre tâche '${data.title}' est due demain.`);
        })

}

function loadNewTask() {
    console.log('1')
    fetch('/tasks/new_task')
        .then(response => response.text())
        .then(data => {
            displayModal(data);
            const dateInput = document.querySelector('#due_date');
            const calendarButton = document.querySelector('#calendar-button')
            const form = document.getElementById('task-form');

            flatpickr(dateInput, {
                dateFormat: "Y-m-d", // Format de la date
                minDate: "today",    // Dates à partir d'aujourd'hui
                altInput: true,      // Ajoute un champ stylisé
                weekNumbers: true,
            });
            calendarButton.addEventListener('click', function () {
                dateInput._flatpickr.open();
            });

            document.addEventListener("DOMContentLoaded", function () {
                const form = document.querySelector('form');

                form.addEventListener('submit', function (e) {
                    e.preventDefault();  

                    
                    fetch(form.action, {
                        method: 'POST',
                        body: new FormData(form),
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data)

                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                });
            });


            document.getElementById('showToastBtn').addEventListener('click', function () {
                const toastLiveExample = document.getElementById('liveToast');
                const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
                toastBootstrap.show();  
            });


        })
        .catch(error => console.error('Error fetching new task:', error));
}

/**
 * Displays the content in a Bootstrap modal and attaches optional event handlers.
 */
function displayModal(content, onCloseCallback) {
    document.getElementById('modal-body-content').innerHTML = content;
    const taskModal = new bootstrap.Modal(document.getElementById('taskModal'), { keyboard: false });
    taskModal.show();

    if (onCloseCallback) {
        document.querySelector('#form').addEventListener('submit', event => {
            event.preventDefault();
            onCloseCallback();
        });
    }
}
