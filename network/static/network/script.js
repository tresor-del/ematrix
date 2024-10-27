document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('#post_id').forEach(button =>{   
        button.addEventListener('click', function(){

            const value = button.value;
            const content = document.querySelector(`#content-${value}`).textContent;
            console.log(content)

            const textarea = document.createElement('textarea');
            textarea.textContent = `${content}`;
            textarea.className = 'p-3';
            textarea.style.display = 'inline';
            textarea.style.width = '100%'

            const button1 = document.createElement('a');
            button1.setAttribute('href', '#')
            button1.textContent = 'Save';
            button1.className = 'p-0';
            button1.style.background = 'none';
            button1.style.border = 'none';
            button1.style.display = 'inline'

            const p = document.createElement('p');
            const p2 = document.createElement('p');
            const p3 = document.createElement('p');
            const p4 = document.createElement('p');

            const referenceButton = document.querySelector(`.post-button-${value}`);
            referenceButton.replaceWith(button1);
            const refercencePost = document.querySelector(`.post-b-${value}`);
            refercencePost.replaceWith(textarea);
            const refercenceP =  document.querySelector(`.comment-icon-${value}`);
            refercenceP.replaceWith(p);
            const refercenceP2 =  document.querySelector(`.like-b-${value}`);
            refercenceP2.replaceWith(p2);
            const refercenceP3 =  document.querySelector(`.total-likes-${value}`);
            refercenceP3.replaceWith(p3);
            const refercenceP4 =  document.querySelector(`.hr-${value}`);
            refercenceP4.replaceWith(p4);

            

            button1.addEventListener('click', function(){

                const newContent = textarea.value;
                console.log(newContent);
                fetch(`/edit/${value}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        'content': newContent
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data)  
                    if (data.success) {
                        textarea.replaceWith(refercencePost)
                        document.querySelector(`#content-${value}`).innerHTML = newContent;
                        button1.replaceWith(referenceButton);
                        p.replaceWith(refercenceP);
                        p2.replaceWith(refercenceP2);
                        p3.replaceWith(refercenceP3);
                        p4.replaceWith(refercenceP4);
                    } else {
                      alert(data.error);
                    }
                });
            });
        });
    });


    document.querySelectorAll('.icon').forEach(icon =>{
        icon.addEventListener('click', function(){
            const id = this.dataset.id 
            console.log(id)

            fetch(`/likes/${id}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                const color = document.querySelector(`.icon-${id}`)
                if (color.style.color === "red"){
                    color.style.color = 'black';
                    document.querySelector(`#like-${id}`).innerHTML = data.total_likes;
                } else{
                    color.style.color = 'red'
                    document.querySelector(`#like-${id}`).innerHTML = data.total_likes;
                }
            })
        })
    })

    const navLinks = document.querySelectorAll('.nav-link');
    const currentUrl = window.location.href;

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
        link.classList.add('v');
    }

    link.addEventListener('click', function() {
        navLinks.forEach(nav => nav.classList.remove('v'));
        this.classList.add('v');
    });
  });

  const s = document.querySelector('#submit');
  s.disabled = true;
  const t = document.querySelector('.new-post-text');
  t.onkeyup = () =>{
    if (t.value.length > 0)
        s.disabled = false;
    else 
        s.disabled = true;
        
        
  }
});