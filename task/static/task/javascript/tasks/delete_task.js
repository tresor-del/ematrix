document.addEventListener('DOMContentLoaded', function(){

    const deleteBtns = document.querySelectorAll('.delete');

        deleteBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            console.log('Delete button clicked');
            const taskId = this.dataset.id;

            // Send a POST request to delete the task
            fetch(`/delete_task/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
            })
            .then(response => {
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);

                // Remove the task element from the DOM
                this.parentElement.remove();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while trying to delete the task.');
            });
        });
        });


})