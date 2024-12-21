document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.remove-friend').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.id;
            const userCard = this.closest('.card');
            console.log(userId)
            fetch('/remove_friend/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                },
                body: JSON.stringify({ id: parseInt(userId) })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert( 'you remove this friend from you friends list')
                    userCard.remove();
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

