
document.addEventListener('DOMContentLoaded',function(){

    
    document.querySelector('#bp').addEventListener('click', function(){
        loadProfilePage();
    })


})

function displayModal(content, onCloseCallback) {
    document.getElementById('modal-body-content').innerHTML = content;
    const taskModal = new bootstrap.Modal(document.getElementById('taskModal'), { keyboard: false });
    taskModal.show();

    if (onCloseCallback) {
        document.querySelector('#form').addEventListener('submit', event => {
            event.preventDefault();
            onCloseCallback();
        });
    }
}

function loadProfilePage(){
    fetch('/edit_profile')
    .then(response =>response.text())
    .then(data =>{
        displayModal(data)
        const profileInput = document.getElementById('profile_image');
        const previewImage = document.getElementById('preview-image');

        profileInput.addEventListener('change', function (event) {
            const file = event.target.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                };

                reader.readAsDataURL(file);
            }
        })
        
    })
}
