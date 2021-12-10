document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_orderbox('inbox'));
	document.querySelector('#archive').addEventListener('click', () => load_orderbox('archive'));
  
	// By default, load the inbox
	load_orderbox('inbox');
  });

  function load_orderbox(orderbox) {
	
	// Show the orderbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#load-email').style.display = 'none';
	document.querySelector('#table-top').style.display = 'block';
  
	// Show inbox and archive (active) button and bottom_line
	document.querySelector('#emails-view').innerHTML = ``;
	$(`#inbox`).removeClass('active_mail');
	$(`#archive`).removeClass('active_mail');
	$(`#${orderbox}`).addClass('active_mail');
	$(`#bottom_line`).removeClass('bottom_line_inbox');
	$(`#bottom_line`).removeClass('bottom_line_archive');
	$(`#bottom_line`).addClass('bottom_line_' + `${orderbox}`);

	fetch(`/order/${orderbox}`, {
	  method: 'GET'
	})
	.then(response => response.json())
	.then(orders => {
		if(orders.length == 0) {
			const email_div = document.createElement('div');
			email_div.innerHTML = "Noch keine Bestellung vorhanden";
			document.querySelector('#emails-view').appendChild(email_div);
		}
		orders.forEach(order => {
			if(order.archieved && orderbox == 'inbox') {
				return false;
			} else {

				// add orderbox content
				const email_div = document.createElement('div');
				email_div.setAttribute("class", "row mb-3 mt-1 ms-2");
				email_div.setAttribute("id", `email_div_${order.id}`);
				email_div.innerHTML += "<div id='subject' class='col-sm-4 col-md-4 col-lg-7 themed-grid-col'>" + order.id + "</div>";
				email_div.innerHTML += "<div class='col-sm-3 col-md-3 col-lg-3 themed-grid-col' style='text-align: right'>" + order.date_ordered + "</div>";
				email_div.innerHTML += "<div id='read' class='col-sm-2 col-md-2 col-lg-1 themed-grid-col'></div>";
				email_div.innerHTML += "<div id='archive' class='col-sm-2 col-md-3 col-lg-1 themed-grid-col'></div>";
				document.querySelector('#emails-view').appendChild(email_div);
				email_div.innerHTML += "<hr class='mt-2'>";
				email_div.querySelector('#subject').addEventListener('click', function () {
					load_order(order)
				})

				if(orderbox != 'sent') {
					// read icon
					const read_icon = document.createElement('i');
					read_icon.setAttribute("aria-hidden", "true");
					if(order.processed == true) {
						read_icon.setAttribute("class", "fa fa-check-square-o");
					} else {
						read_icon.setAttribute("class", "fa fa-square-o");
						document.querySelector(`#email_div_${order.id} #subject`).style.fontWeight = "900";
					}
					document.querySelector(`#email_div_${order.id} #read`).appendChild(read_icon);
					read_icon.addEventListener('click', () => {
						fetch('/order/'+`${order.id}`, {
							method: 'PUT',
                            headers:{
                                'X-CSRFToken': csrftoken,
                            },
							body: JSON.stringify({
								processed: !(order.processed)
							})
						})
						.then(() => load_orderbox('inbox'));
					})
					//archive button
					const archive_btn = document.createElement('i');
					archive_btn.setAttribute("class", "fa fa-archive");
					archive_btn.setAttribute("aria-hidden", "true");
					document.querySelector(`#email_div_${order.id} #archive`).appendChild(archive_btn);
					archive_btn.addEventListener('click', () => {
						fetch('/order/'+`${order.id}`, {
							method: 'PUT',
                            headers:{
                                'X-CSRFToken': csrftoken,
                            },
							body: JSON.stringify({
								archived: !(order.archived)
							})
						})
						.then(() => load_orderbox('inbox'));
					})
				}
			}
		})
	})
  }
  
  function load_order(order) {
  
	// Show the orderbox and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#load-email').style.display = 'block';
	document.querySelector('#table-top').style.display = 'none';
  
	fetch('/order/'+`${order.id}`)
	.then(response => response.json())
	.then(order => {
  
		// Show subject of the email
		document.querySelector('#load-email').innerHTML = `<h3>Auftrags-ID: ${order.id}</h3>`;
	
		const date_div = document.createElement('div');
		date_div.setAttribute("class", "border mt-2 p-3");
        date_div.innerHTML += "Benutzername: " + order.user + "<br />";
		date_div.innerHTML += "Datum: " + order.date_ordered + "<br />";

        const cart_id_div = document.createElement('div');
		cart_id_div.setAttribute("class", "border mt-2 p-3");
		cart_id_div.innerHTML += "Bestellnummer: " + order.cart_id + "<br />";
  
		const body_div = document.createElement('div');
		body_div.setAttribute("class", "border mt-2 mb-2 p-3");
        body_div.innerHTML += "<div class='cart-row'><div style='flex:2'><strong>Item</strong></div><div style='flex:1'><strong>Price</strong></div><div style='flex:1'><strong>Anzahl</strong></div><div style='flex:1'><strong>Gesamtpreis</strong></div>";
        for(var i = 0; i < order.listings.length; i++) {
            body_div.innerHTML += "<div class='cart-row mt-4'><div class='pt-2' style='flex:2'><p>" + order.listings[i] + "</p></div><div class='pt-2' style='flex:1'><p>" + order.price[i] + "€</p></div><div style='flex:1'><div class='qty mt-1'>" + order.quantity[i] + "</div></div><div style='flex:1'><p>" + order.total_price_listing[i] + "€</p></div></div>";
        }
        body_div.innerHTML += "<hr />";
        body_div.innerHTML += "<div class='cart-row mt-4'><div class='pt-2' style='flex:2'></div><div class='pt-2' style='flex:1'></div><div style='flex:1'><div class='qty mt-1'><strong>" + order.total_amount + "</strong></div></div><div style='flex:1'><p><strong>" + order.total_price + "€</strong></p></div></div>";

        const address_div = document.createElement('div');
		address_div.setAttribute("class", "border mt-2 p-3");
        address_div.innerHTML += "Adresse: <br />";
		address_div.innerHTML += order.address_name + "<br />";
        address_div.innerHTML += order.address_address + "<br />";
        address_div.innerHTML += order.address_zipcode + ", " + order.address_city;

		const back_btn = document.createElement('button');
		back_btn.setAttribute("class", "btn btn-primary");
		back_btn.textContent = "Aufträge";
		document.querySelector('#load-email').appendChild(back_btn);
		back_btn.addEventListener('click', () => {
			load_orderbox('inbox');	
		}); 

		document.querySelector('#load-email').appendChild(date_div);
        document.querySelector('#load-email').appendChild(cart_id_div);
		document.querySelector('#load-email').appendChild(body_div);
        document.querySelector('#load-email').appendChild(address_div);

	});
}


