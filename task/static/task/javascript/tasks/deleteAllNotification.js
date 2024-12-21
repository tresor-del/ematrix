document.addEventListener('DOMContentLoaded', function(){

   // Delete all notifications
   const deleteAllButton = document.querySelector('.delete-all');
   if (deleteAllButton) { // Check if the delete-all button exists
       deleteAllButton.addEventListener('click', function () {
           const confirmation = confirm('Are you sure you want to delete all notifications?'); // Confirm the action
           if (confirmation) {
               // Send a GET request to delete all notifications on the server
               fetch('/delete_all_notification')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Network response was not ok'); // Handle unsuccessful requests
                   }
                   return response.json(); // Parse the JSON response
               })
               .then(data => {
                   console.log('Response data:', data); // Log the server's response

                   // Remove all notification elements from the DOM
                   document.querySelectorAll('.notification').forEach(div => {
                       div.remove();
                   });

                   // Create a placeholder message indicating no notifications are available
                   const div = document.createElement('div');
                   div.className = 'alert alert-warning text-center';
                   div.innerHTML = `
                       <span style="font-size: 2rem;">📭</span>
                       <p class="mt-3 mb-0">No notifications available right now. Stay tuned!</p>
                   `;

                   // Remove the delete-all button
                   deleteAllButton.remove();

                   // Append the placeholder message to the notifications container
                   document.getElementById('notifications-container').appendChild(div);
               })
               .catch(error => {
                   console.error('Error:', error); // Log any errors
                   alert('An error occurred while trying to delete the task.'); // Notify the user of the error
               });
           }
       });
   }

})