gsap.registerPlugin(ScrollTrigger);

gsap.defaults({
    duration: 1.5,
    opacity: 0
});

gsap.from('.container-fluid',{ 
    scale: 0.1,
    stagger: {
        from: 'bottom'
    }
});

gsap.from('.showcase-left',{ y: -100});

gsap.from('.showcase-right',{ x: 100});

gsap.from('.showcase-btn', {
    delay: 0,
    scale: 0.1,
    stagger: {
        from: 'bottom'
    }
})

gsap.from('#quote div',{
    scale: 0.1,
    stagger: {
        from: 'bottom'
    }
})

gsap.from('#info-left1',{ 
    x: -100,
    scrollTrigger: '#info1'
})

gsap.from('#info-right1',{ 
    x: 100,
    scrollTrigger: '#info1'
})

gsap.from('.info-2',{ 
    y: 100,
    scrollTrigger: '#info2'
})

// Clear out composition fields
document.querySelector('#compose-question-subject').value = '';
document.querySelector('#compose-question-body').value = '';

document.querySelector('#compose-question-form').onsubmit = function (event) {

  event.preventDefault();

  const Subject = document.querySelector('#compose-question-subject').value;
  const Body = document.querySelector('#compose-question-body').value;
  document.querySelector('#messages').innerHTML = '';

  fetch("/emails", {
    method: 'POST',
    body: JSON.stringify({
        recipients: 'admin@admin.com',
        subject: Subject,
        body: Body
    })
  })
  .then(response => response.json())
  .then(message => {
    const br = document.createElement('br');
    const messages_div = document.createElement('div');
    json = JSON.stringify(message)
    replaced_message = json.replace('{"message":"', '');
    replaced_message1 = replaced_message.replace('"}', '');
    if(JSON.stringify(message) == '{"message":"Anfrage erfolgreich gesendet."}'){
        messages_div.setAttribute("id", "show_message");
        messages_div.setAttribute("class", "alert alert-success");
        messages_div.innerHTML += replaced_message1;
    } else {
        messages_div.setAttribute("id", "show_message");
        messages_div.setAttribute("class", "alert alert-danger");
        messages_div.innerHTML += replaced_message1;
    }

    document.querySelector('#messages').appendChild(br);
    document.querySelector('#messages').appendChild(messages_div);

    window.setTimeout("document.querySelector('#show_message').style.display='none'", 3000);
    
  })
  
  document.querySelector('#compose-question-subject').value = '';
  document.querySelector('#compose-question-body').value = '';
} 
