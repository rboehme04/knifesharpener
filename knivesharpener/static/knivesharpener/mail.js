document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#archive').addEventListener('click', () => load_mailbox('archive'));
  
	// By default, load the inbox
	load_mailbox('inbox');
  });
  
  function compose_email() {
  
	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';
	document.querySelector('#load-email').style.display = 'none';
	document.querySelector('#table-top').style.display = 'none';
	document.querySelector('#title-mail').innerHTML = 'Neue Email erstellen';
  
	// Clear out composition fields
	document.querySelector('#compose-recipients').value = '';
	document.querySelector('#compose-subject').value = '';
	document.querySelector('#compose-body').value = '';
  
	document.querySelector('#compose-form').onsubmit = function (event) {
  
	  event.preventDefault();
  
	  const Recipients = document.querySelector('#compose-recipients').value;
	  const Subject = document.querySelector('#compose-subject').value;
	  const Body = document.querySelector('#compose-body').value;
  
	  fetch("/emails", {
		method: 'POST',
		body: JSON.stringify({
			recipients: Recipients,
			subject: Subject,
			body: Body
		})
	  })
	  .then(response => response.json())
	  .then(result => {
		  load_mailbox('sent', result);
	  })
	  .catch(error => {
		console.log(error);
	  })
	} 
  }

  function load_mailbox(mailbox) {
	
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#load-email').style.display = 'none';
	document.querySelector('#table-top').style.display = 'block';
  
	// Show inbox and archive (active) button and bottom_line
	document.querySelector('#emails-view').innerHTML = ``;
	$(`#inbox`).removeClass('active_mail');
	$(`#archive`).removeClass('active_mail');
	$(`#${mailbox}`).addClass('active_mail');
	$(`#bottom_line`).removeClass('bottom_line_inbox');
	$(`#bottom_line`).removeClass('bottom_line_archive');
	$(`#bottom_line`).addClass('bottom_line_' + `${mailbox}`);

	// add compose and sent button for admin
	if(user == 'admin'){
		document.querySelector('#admin').innerHTML = '';
		document.querySelector('#admin').style.display = 'block';
		const compose_btn = document.createElement('button');
		compose_btn.setAttribute("class", "btn btn-sm btn-outline-primary");
		compose_btn.setAttribute("id", 'compose');
		compose_btn.innerHTML = 'Neue Email';
		const sent_btn = document.createElement('button');
		sent_btn.setAttribute("class", "btn btn-sm btn-outline-primary");
		sent_btn.setAttribute("id", 'sent');
		sent_btn.innerHTML = 'Gesendet';
		document.querySelector('#admin').appendChild(compose_btn);
		document.querySelector('#admin').appendChild(sent_btn);

		document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
		document.querySelector('#compose').addEventListener('click', compose_email);
	}

	if(mailbox == 'sent') {
		document.querySelector('#title-mail').innerHTML = 'Gesendet';
	} else {
		document.querySelector('#title-mail').innerHTML = 'Posteingang';
	}

	fetch(`/emails/${mailbox}`, {
	  method: 'GET'
	})
	.then(response => response.json())
	.then(emails => {
		if(emails.length == 0) {
			const email_div = document.createElement('div');
			email_div.innerHTML = "Noch keine Emails vorhanden";
			document.querySelector('#emails-view').appendChild(email_div);
		}
		emails.forEach(email => {
			if(email.archieved && mailbox == 'inbox') {
				return false;
			} else {

				// add mailbox content
				const email_div = document.createElement('div');
				email_div.setAttribute("class", "row mb-3 mt-1 ms-2");
				email_div.setAttribute("id", `email_div_${email.id}`);
				email_div.innerHTML += "<div id='subject' class='col-sm-4 col-md-4 col-lg-7 themed-grid-col'>" + email.subject + "</div>";
				email_div.innerHTML += "<div class='col-sm-3 col-md-3 col-lg-3 themed-grid-col' style='text-align: right'>" + email.timestamp + "</div>";
				email_div.innerHTML += "<div id='read' class='col-sm-2 col-md-2 col-lg-1 themed-grid-col'></div>";
				email_div.innerHTML += "<div id='archive' class='col-sm-2 col-md-3 col-lg-1 themed-grid-col'></div>";
				document.querySelector('#emails-view').appendChild(email_div);
				email_div.innerHTML += "<hr class='mt-2'>";
				email_div.querySelector('#subject').addEventListener('click', function () {
					load_email(email)
				})			
		
				if(mailbox != 'sent') {
					// read icon
					const read_icon = document.createElement('i');
					read_icon.setAttribute("aria-hidden", "true");
					if(email.read == true) {
						read_icon.setAttribute("class", "fa fa-check-square-o");
					} else {
						read_icon.setAttribute("class", "fa fa-square-o");
						document.querySelector(`#email_div_${email.id} #subject`).style.fontWeight = "900";
					}
					document.querySelector(`#email_div_${email.id} #read`).appendChild(read_icon);
					read_icon.addEventListener('click', () => {
						fetch('/emails/'+`${email.id}`, {
							method: 'PUT',
							body: JSON.stringify({
								read: !(email.read)
							})
						})
						.then(() => load_mailbox('inbox'));
					})
					//archive button
					const archive_btn = document.createElement('i');
					archive_btn.setAttribute("class", "fa fa-archive");
					archive_btn.setAttribute("aria-hidden", "true");
					document.querySelector(`#email_div_${email.id} #archive`).appendChild(archive_btn);
					archive_btn.addEventListener('click', () => {
						fetch('/emails/'+`${email.id}`, {
							method: 'PUT',
							body: JSON.stringify({
								archived: !(email.archived)
							})
						})
						.then(() => load_mailbox('inbox'));
					})
				}
			}
		})
	})
  }
  
  function load_email(email) {
  
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#load-email').style.display = 'block';
	document.querySelector('#table-top').style.display = 'none';
	document.querySelector('#admin').style.display = 'none';
  
	fetch('/emails/'+`${email.id}`)
	.then(response => response.json())
	.then(email => {
  
		// Show subject of the email
		document.querySelector('#load-email').innerHTML = `<h3>${email.subject}</h3>`;
	
		const email_div = document.createElement('div');
		email_div.setAttribute("class", "border mt-2 p-3");
		if(email.user == 'admin@admin.com'){
			email_div.innerHTML += "from: " + email.sender + "<br />";
			email_div.innerHTML += "to: ";
			for (let recipient of email.recipients) {
			email_div.innerHTML += recipient;
			}
			email_div.innerHTML += "<br />";
		}
	
		email_div.innerHTML += "Datum: " + email.timestamp + "<br />";
  
		const body_div = document.createElement('div');
		body_div.setAttribute("class", "border mt-2 mb-2 p-3");
		body_div.innerHTML += email.body + "<br />";
		const back_btn = document.createElement('button');
		back_btn.setAttribute("class", "btn btn-primary");
		back_btn.textContent = "Posteingang";
		document.querySelector('#load-email').appendChild(back_btn);
		back_btn.addEventListener('click', () => {
			load_mailbox('inbox');	
		}); 

		document.querySelector('#load-email').appendChild(email_div);
		document.querySelector('#load-email').appendChild(body_div);

		if(email.user == 'admin@admin.com'){
			const reply_btn = document.createElement('button'); // reply button
			reply_btn.setAttribute("class", "btn btn-primary");
			reply_btn.textContent = "Reply";
			document.querySelector('#load-email').appendChild(reply_btn);
	
			reply_btn.addEventListener('click', () => {
			compose_email(); // reply clicked => email composition form
	
			// prefill form (reply case)
			document.querySelector('#compose-recipients').value = email.sender;
			document.querySelector('#compose-subject').value = email.subject.slice(0,4) == 'Re: ' ? 'Re: ' + email.subject.slice(4) : 'Re: ' + email.subject;
			document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote: ' + email.body;
			}); 
		}
	});
  
	 // Set the email to read.
	 fetch(`/emails/${email.id}`, {
	  method: "PUT",
	  body: JSON.stringify({
		read: true
	  })
	});
}


