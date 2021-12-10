var updateBtns = document.querySelectorAll('.update-cart')

 for(var i = 0; i < updateBtns.length; i++) {
     updateBtns [i].addEventListener('click', function(){
        var listingId = this.dataset.listing
        var action = this.dataset.action
        console.log('listingId: ', listingId, 'action: ', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in');
            window.location.href = 'login'
        } else {
            updateUserCart(listingId, action)
        }
     })
 }

 function updateUserCart(listingId, action){
     console.log('User is loggen in, sending data..')

     fetch('/update_listing', {
        method: 'POST',
        headers:{
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'listingId': listingId,
            'action': action
        })
     })
     .then((response) => {
         return response.json()
     })
     .then((data) =>{
         console.log('data: ', data)
         location.reload()
     })
 }