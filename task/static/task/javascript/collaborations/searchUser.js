document.addEventListener('DOMContentLoaded', function(){
        const searchInput = document.getElementById('search');
        const searchButton = document.getElementById('search-button');
        const resultsContainer = document.getElementById('results');
        const loadingIndicator = document.getElementById('loading');
        const noResultsMessage = document.getElementById('no-results');
    
        // Fonction pour afficher les utilisateurs
        const displayUsers = (users) => {
            const resultsDiv = resultsContainer.querySelector('.results-container');
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
                    <div class="row g-0 align-items-center " id='invite-container-${user.id}'>
                        <div class="col-auto p-3">
                            <img src="${user.profile_image}" class='rounded-circle' >
                        </div>
                        <div class="col">
                            <div class="card-body p-2">
                                <h5 class="card-title mb-1">${user.username}</h5>
                            </div>
                        </div>
                        <div class="col-auto me-3">
                            <button class="btn btn-sm btn-success invite-btn" data-user-id="${user.id}">
                                <i class="bi bi-person-plus"></i> Invite
                            </button>
                        </div>
                    </div>
                `;
            
                // Ajout de l'événement au bouton
                const inviteButton = userCard.querySelector('.invite-btn');
                inviteButton.addEventListener('click', () => inviteUser(user.id));
            
                // Ajout de la carte dans le conteneur des résultats
                resultsDiv.appendChild(userCard);
            });
            
        };
    
        // Fonction pour rechercher les utilisateurs
        const searchUsers = () => {
            const query = searchInput.value.trim();
            if (!query) return;
    
            loadingIndicator.style.display = 'block';
    
            fetch(`/collaborations/search_users?search=${query}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    loadingIndicator.style.display = 'none';
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
    
        // Fonction pour inviter un utilisateur
        const inviteUser = (userId) => {
            

            fetch(`/invite_user/${userId}`)
            .then( response => response.json())
            .then( result => {
                console.log(result)
                alert(`Invitation sent successfully`);
                const container = document.getElementById(`invite-container-${userId}`);
                        const button = container.querySelector('.invite-btn');
                        button.innerHTML = `
                            <i class="bi bi-check-circle text-success"></i> Invitation sent
                        `;
            })
        };
    
        searchButton.addEventListener('click', searchUsers);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchUsers();
            }
        });
    });
    
