document.addEventListener('DOMContentLoaded', function(){

    const createNewProjectButton = document.querySelector('#create-task');
    createNewProjectButton.addEventListener('click', function(){
        loadNewProjectTask(this.dataset.id);
    })

})

function loadNewProjectTask(projectId) {
    console.log('1')
    fetch(`/project/${projectId}/new_task`)
        .then(response => response.text())
        .then(data => {
            displayModal(data);
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