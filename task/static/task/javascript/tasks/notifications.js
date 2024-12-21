document.addEventListener('DOMContentLoaded', function () {

   // Select the notification button and its child span
   const notificationButton = document.querySelector('#notificationButton');
   const span = notificationButton.querySelector('span');

   // Event listener to remove the span when the notification button is clicked
   notificationButton.addEventListener('click', function () {
       notificationButton.removeChild(span);
   });


});
