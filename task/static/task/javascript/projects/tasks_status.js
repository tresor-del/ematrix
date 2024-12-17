document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.status').forEach( btn => {
        btn.addEventListener('click', function(){
            const project = document.querySelector('#project');
            const projectId = project.dataset.id
            changeStatus(this.dataset.status, projectId, this.dataset.id);
        });
    });


function changeStatus(status, projectId, taskId ){
    fetch(`/project/${projectId}/task/${taskId}/status`, {
        method: 'PUT',
        body: JSON.stringify({
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.querySelector('#status').innerHTML= status;
    })

    

}

});