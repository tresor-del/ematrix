document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.status').forEach( btn => {
        btn.addEventListener('click', function(){
            const project = document.querySelector('#project-name');
            const projectId = project.dataset.id
            changeStatus(btn, this.dataset.status, projectId, this.dataset.id);
        });
    });


function changeStatus(element,status, projectId, taskId ){
    console.log(element)
    fetch(`/project/${projectId}/task/${taskId}/status`, {
        method: 'PUT',
        body: JSON.stringify({
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (status === 'Completed'){
            Swal.fire({
                title: 'Task Completed',
                text: 'Congratulation for completing this task. You are on the right way',
                icon: 'success',
                confirmButtonText: 'Got it!',
                customClass: {
                    popup: 'custom-popup',
                    title: 'custom-title',
                    confirmButton: 'custom-button'
                }
            });
        }
        
        element.closest('.task').querySelector('.new-status').innerHTML = status;
    })

    

}

});