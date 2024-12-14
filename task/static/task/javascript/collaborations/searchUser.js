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
                const userElement = document.createElement('div');
                userElement.textContent = user.username;
                userElement.dataset.userId = user.id;
    
                // Ajouter un bouton pour inviter
                const inviteButton = document.createElement('button');
                inviteButton.textContent = 'Invite';
                inviteButton.className = 'btn btn-sm btn-success ';
                inviteButton.addEventListener('click', () => inviteUser(user.id));
    
                userElement.appendChild(inviteButton);
                resultsDiv.appendChild(userElement);
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
                alert(`Invitation envoyée à l'utilisateur avec ID ${userId}`);
            })
        };
    
        searchButton.addEventListener('click', searchUsers);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchUsers();
            }
        });
    });
    
