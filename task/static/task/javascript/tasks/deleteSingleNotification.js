document.addEventListener('DOMContentLoaded', function(){

// Delete a single notification
document.querySelectorAll('.delete-notification').forEach(button => {
    button.addEventListener('click', function () {
        const notificationId = this.getAttribute('data-id'); // Get notification ID from data attribute
        alert(`Notification with ID ${notificationId} deleted.`); // Show a deletion confirmation message

        // Send an AJAX POST request to delete the notification on the server
        fetch(`/delete_notification/${notificationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok'); // Handle unsuccessful requests
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log('Response data:', data); // Log the server's response

            // Remove the notification element from the DOM
            this.parentElement.remove();
        })
        .catch(error => {
            console.error('Error:', error); // Log any errors
            alert('An error occurred while trying to delete the task.'); // Notify the user of the error
        });
    });
});

});