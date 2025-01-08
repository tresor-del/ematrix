document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#chart').addEventListener('click', function() {

            displayChart();
});

});

function displayChart () {
    fetch('/task/chart')
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch task data");
        }
        return response.text();
    })
    .then(data => {
        console.log(data);
        displayModal(data);

         // Initialize the chart
         var ctx = document.getElementById('tasksChart').getContext('2d');
         var completed_task_count = parseInt(document.getElementById('c').textContent.trim());
         var pending_task_count = parseInt(document.getElementById('p').textContent.trim());
 
         var tasksChart = new Chart(ctx, {
             type: 'doughnut',
             data: {
                 labels: ['Completed', 'Pending'],
                 datasets: [{
                     label: 'Tasks Statistics',
                     data: [completed_task_count, pending_task_count],
                     backgroundColor: ['#28a745', '#ffc107']
                 }]
             },
             options: {
                 responsive: true,
                 maintainAspectRatio: false,
                 plugins: {
                     legend: {
                         display: true,
                         position: 'bottom'
                     },
                     tooltip: {
                         callbacks: {
                             label: function (tooltipItem) {
                                 const value = tooltipItem.raw;
                                 const total = tasksChart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                 const percentage = ((value / total) * 100).toFixed(2);
                                 return `${tooltipItem.label}: ${value} (${percentage}%)`;
                             }
                         }
                     }
                 }
             }
         });

         // Make the chart smaller
         document.getElementById('tasksChart').style.width = '300px';
         document.getElementById('tasksChart').style.height = '300px';
 
         function updateChart() {
             const completed = parseInt(document.getElementById('c').textContent.trim());
             const pending = parseInt(document.getElementById('p').textContent.trim());
 
             tasksChart.data.datasets[0].data = [completed, pending];
             tasksChart.update();
         }
 
         function changeTaskCounts() {
             updateChart();
         }
         setInterval(changeTaskCounts, 1000);

    })

    .catch(error => {
        console.error("Error:", error);
    });

};
