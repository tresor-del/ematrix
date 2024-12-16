document.addEventListener('DOMContentLoaded', function(){

    const EditProjectButton = document.querySelector('#edit-project');
    EditProjectButton.addEventListener('click', function(){

        loadEditProject(this.dataset.id);
    })

})

function loadEditProject(projectId) {

    fetch(`/project/edit_project/${projectId}`)
        .then(response => response.text())
        .then(data => {
            displayModal(data);
        })
        .catch(error => console.error('Error fetching edit project:', error));
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