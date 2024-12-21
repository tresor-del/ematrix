document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#project-form');
    const submitButton = document.querySelector('#project-btn');
    const projectStatusBtn = document.querySelectorAll('.project-status');
    const changeNameBtn = document.querySelector('#change-name-btn');
    const changeDescBtn  = document.querySelector('#change-description-btn');


    document.getElementById('comment-btn').addEventListener('click', function (event) {
        console.log('comment btn clicked')
        event.preventDefault();
        const form = document.getElementById('comment-form');
        const formData = new FormData(form);
    
        PostComment(form, formData)
        // Ajout d'un indicateur de chargement
        const button = document.getElementById('comment-btn');
        button.disabled = true;
        button.textContent = 'Posting...';
    });


    submitButton.addEventListener('click', function (event) {
        alert('btn clicked')
        event.preventDefault(); 
        createProject(form);
    });


    changeNameBtn.addEventListener('click', function () {
        const projectId = document.querySelector('#project-name').getAttribute('data-id');
        const newName = document.querySelector('#new-name').value.trim();

        if (newName) {
            changeProjectName(projectId, newName);
        } else {
            alert('Project name cannot be empty.');
        }
    });

    changeDescBtn.addEventListener('click', function () {
        const projectId = document.querySelector('#project-name').getAttribute('data-id');
        const newDesc = document.querySelector('#new-description').value.trim();

        changeProjectDesc(projectId, newDesc);
    });


    projectStatusBtn.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
    
            const projectId = this.dataset.id;
            const newStatus = this.dataset.status;
    
            changeProjectStatus(projectId, newStatus);
        });
    });

    

});

function createProject(form) {
    const action = form.action; // URL d'action du formulaire
    const data = new FormData(form); // Récupère les données du formulaire

    fetch(action, {
        method: 'POST',
        body: data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse la réponse JSON
    })
    .then(data => {
        if (data.project) {
            const { name: title, status: projectStatus, members, id : id } = data.project;

            // Ajouter dynamiquement le projet au DOM
            const projectContainer = document.querySelector('#project-container');
            if (projectContainer) {
                const div = document.createElement('div');
                div.className = "col-12 col-md-6 col-lg-4 mb-4 project-item";
                div.innerHTML = `
                    <a href="/project/project_detail/${id}" style="color: black; text-decoration: none;">
                    <div class="card shadow-lg border-light">
                        <div class="card-body">
                            <h5 class="card-title text-primary title">${title} <small class="fs-6">(${projectStatus})</small></h5>
                            <small class="mb-2">${members} members</small>
                        </div>
                    </div>
                    </a>
                `;
                projectContainer.appendChild(div);
            } else {
                console.error("Le conteneur #project-container est introuvable.");
            }

            // Réinitialiser le formulaire après succès
            form.reset();
        } else if (data.errors) {
            console.error("Erreur dans le formulaire :", data.errors);
        } else {
            console.error("Aucune donnée de projet retournée.");
        }
    })
    .catch(error => {
        console.error("Une erreur est survenue :", error);
    });
}

function changeProjectStatus(projectId, newStatus) {
    fetch(`/project/change-status/${projectId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ newStatus: newStatus }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                document.querySelector('#current-status').innerHTML = newStatus;
            } else {
                console.error('Erreur côté serveur :', data.error || 'Statut non changé.');
            }
        })
        .catch(error => {
            console.error('Une erreur est survenue :', error);
        });
}

function changeProjectName(projectId,newName){
    fetch(`/project/edit_project/${projectId}`, {
        method: 'POST',
        body: JSON.stringify({
            newName: newName
        })
    })
        .then(response => response.json())
        .then(data => {
            if(data.message){
                console.log(data.message)
                document.querySelector('#project-name').innerHTML = newName
            }
            
            
        })
        .catch(error => console.error('Error fetching edit project:', error));

}

function changeProjectDesc(projectId,newDesc){
    fetch(`/project/edit_project/${projectId}`, {
        method: 'POST',
        body: JSON.stringify({
            description: newDesc
        })
    })
        .then(response => response.json())
        .then(data => {
            if(data.message){
                console.log(data.message)
                document.querySelector('#project-description').innerHTML = newDesc
            }
            
            
        })
        .catch(error => console.error('Error fetching edit project:', error));

}


function PostComment(form, formData){
    const button = document.getElementById('comment-btn');
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
        .then(response => {
            button.disabled = false;
            button.textContent = 'Post Comment';
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.message) {
                const commentContainer = document.getElementById('comment-container');
                const newComment = document.createElement('div');
                newComment.classList.add('mb-3', 'd-flex', 'align-items-start');
                newComment.innerHTML = `
                    <img src="${data.comment.profile_image}" alt="${data.comment.author}'s profile picture" class="rounded-circle border me-2" style="width: 40px; height: 40px; object-fit: cover;">
                    <div>
                        <strong>${data.comment.author}</strong> <small>${data.comment.created_at}</small>
                        <p>${data.comment.comment}</p>
                    </div>
                `;
                commentContainer.appendChild(newComment);
                form.reset();
            } else {
                alert('Failed to post comment.');
            }
        })
        .catch(error => {
            button.disabled = false;
            button.textContent = 'Post Comment';
            console.error('Error:', error);
            alert('An error occurred while posting the comment.');
        });
        return false;
}
    

