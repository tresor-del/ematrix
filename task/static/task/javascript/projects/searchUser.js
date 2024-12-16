document.addEventListener('DOMContentLoaded', function(){
    const searchInput = document.getElementById('usernameInput');
    const searchButton = document.getElementById('addMemberBtn');
    const resultsContainer = document.getElementById('presults');
    const noResultsMessage = document.getElementById('pno-results');

    // Fonction pour afficher les utilisateurs
    const displayUsers = (users) => {
        const resultsDiv = resultsContainer.querySelector('.presults-container');
        resultsDiv.innerHTML = '';
        if (users.length === 0) {
            noResultsMessage.style.display = 'block';
            return;
        }
        noResultsMessage.style.display = 'none';

        users.forEach(user => {
            // Création de la carte utilisateur
            const userCard = document.createElement('div');
            userCard.className = 'card mb-3 shadow-sm';
            userCard.style.maxWidth = '500px';
        
            // Contenu de la carte
            userCard.innerHTML = `
                <div class="row g-0 align-items-center " id='invite-container-{{ user.id }}'>
                    <div class="col">
                        <div class="card-body p-2">
                            <h5 class="card-title mb-1">${user.friends__username}</h5>
                        </div>
                    </div> 
                    <div class="col-auto me-3">
                        <button class="btn btn-sm btn-success " id='add-btn' data-id="${user.friends__id}">
                            <i class="bi bi-person-plus"></i> Add
                        </button>
                    </div>
                </div>
            `;
        
            // Ajout de l'événement au bouton
            const inviteButton = userCard.querySelector('#add-btn');
            inviteButton.addEventListener('click', () => addMember(user.id));
        
            // Ajout de la carte dans le conteneur des résultats
            resultsDiv.appendChild(userCard);
        });
        
    };

    // Fonction pour rechercher les utilisateurs
    const searchUsers = () => {
        const query = searchInput.value.trim();
        if (!query) return;


        fetch(`/project/search_members?search=${query}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                displayUsers(data.users);
                document.querySelector('#search-button').addEventListener('click',function(){
                    document.querySelector('#search').value = '';
                    
                })
            })
            .catch(error => {
                loadingIndicator.style.display = 'none';
                console.error('Erreur :', error);
                alert('Une erreur s\'est produite lors de la recherche.');
                
            });
    };

    // Add member via AJAX
    function addMember (userId) {
        const projectId = document.querySelector('#project').dataset.id;
        fetch(`/project/${projectId}/add_member/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({ userId : userId  }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload(); // Reload the page to update the member list
            } else if (data.error) {
                alert(data.error);
            }
        });
    };

    document.querySelectorAll('.removeMemberBtn').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.dataset.id;
            const projectId = document.querySelector('#project').dataset.id;
            fetch(`/project/${projectId}/remove_member/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: JSON.stringify({ userId: userId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload(); // Reload the page to update the member list
                } else if (data.error) {
                    alert(data.error);
                }
            });
        });
    });

    searchButton.addEventListener('click', searchUsers);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchUsers();
        }
    });
});

