document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Sending emails handler
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});





function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id){

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    console.log(email)

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-detail-view').style.display = 'block';

    document.querySelector('#emails-detail-view').innerHTML=`
    <ul class= 'list-group'>
      <li class= 'list-group-item'><strong>From: </strong> ${email.sender} </li>
      <li class= 'list-group-item'><strong>To:</strong> ${email.recipients} </li>
      <li class= 'list-group-item'><strong>Subject: </strong> ${email.subject} </li>
      <li class= 'list-group-item'><strong>Timestamp: </strong> ${email.timestamp} </li>
      <li class= 'list-group-item'>${email.body} </li>
    </ul>
    `
    if (!email.read){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

    const btn_arch = document.createElement('button');
    btn_arch.innerHTML = email.archived ? 'Unarchived': 'Archived';
    btn_arch.className = email.archived ? 'btn btn-success' : 'btn btn-danger';
    btn_arch.addEventListener('click', function(){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {
        load_mailbox('archive')
      })
    });

      if(document.querySelector('h3').innerHTML != 'Sent'){
        document.querySelector('#emails-detail-view').append(btn_arch);
      }
    


    const btn_reply = document.createElement("button");
    btn_reply.innerHTML =  'Reply';
    btn_reply.className = 'btn btn-info margin';
    btn_reply.addEventListener('click', function (){
      compose_email();

      document.querySelector('#compose-recipients').value = `${email.sender}`;
      let subject = email.subject;
      document.querySelector('#compose-subject').value = subject.startsWith('Re: ') ? subject : `Re: ${subject}`;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`;

    });
    document.querySelector('#emails-detail-view').append(btn_reply);


  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    
    emails.forEach(email => {

      // for inbox view
      const newEmail = document.createElement('div');

      newEmail.className= 'flex-handler';

      newEmail.innerHTML = `
        <h5 class='display-handler'><strong>${email.sender}</strong></h5>
        <h6 class='display-handler '>${email.subject}</h5> 
        <p class='display-handler item-last '>${email.timestamp}</p>
      `;

      newEmail.className= email.read ? 'read': 'unread';
      
      newEmail.addEventListener('click', function() {
        view_email(email.id);
      });

      // for sent view
      const newEmail2 = document.createElement('div');

      newEmail2.className= 'flex-handler';

      newEmail2.innerHTML = `
        <h5 class='display-handler'>To: <strong>${email.recipients}</strong></h5>
        <h6 class='display-handler '>${email.subject}</h5> 
        <p class='display-handler item-last'>${email.timestamp}</p>
      `;

      newEmail2.className= email.read ? 'read': 'unread';
      
      newEmail2.addEventListener('click', function() {
        view_email(email.id);
      });

      if(document.querySelector('h3').innerHTML === 'Inbox'){
        document.querySelector('#emails-view').append(newEmail);
      } else{
        document.querySelector('#emails-view').append(newEmail2);
      }
      
    })
  });
  
}

function send_email(event){
  event.preventDefault();

  const recipient = document.querySelector('#compose-recipients').value ;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');


  })
}