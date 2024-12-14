document.addEventListener('DOMContentLoaded', function () {


document.querySelector('#notificationsButton').addEventListener('click', function(){
    loadNotifications()
})

function loadNotifications() {   

    fetch('/notifications')
        .then(response => response.text())
        .then(data => {
            displayModal(data);
            span = document.querySelector('#span');
            notificationId = span.dataset.id;
            console.log(notificationId)
            notifId= parseInt(notificationId);
            console.log(notifId)
            fetch('/notifications', {
                method: 'PUT',
                body: JSON.stringify({
                    id: notifId,
                    is_read: true
                })
            })

              // Select all delete buttons
            const deleteBtns = document.querySelectorAll('.delete-btn');

                // Attach click event listeners to each button
                deleteBtns.forEach(btn => {
                    btn.addEventListener('click', function (event) {
                        event.preventDefault(); // Empêcher le comportement par défaut du lien
                        console.log('Delete button clicked');
                
                        const taskId = this.dataset.id; // Récupère l'ID de la tâche
                        console.log(taskId);
                
                        // Envoyer une requête POST pour supprimer la tâche
                        fetch(`/delete_task/${taskId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log('Task deleted successfully:', data);
                
                            // Supprimer l'élément DOM uniquement après un succès
                            this.closest('.alert').remove();
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Failed to delete the task. Please try again.');
                        });
                    });
                });
                
            
        })
        .catch(error => console.error('Error fetching task details:', error));
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


})