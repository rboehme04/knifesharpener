# Capstone project by Richard Böhme

### About:
The project I chose for the capstone project is a type of e-commerce store where you can order services and communicate with the site administrator through a built-in messenger function.  
The user can view the homepage and read the information about the knife sharpening store. He can also view the offers presented on another page. It is possible for the user to register or log in through the login page. Once the user is logged in, he has the possibility to send a request to the administrator of the site via a contact form and ask him a question. This request will end up in the administrator's inbox. The administrator of the page can reply to the request, send new messages and view the sent messages. Each user has a messenger page. The messenger is divided into the inbox and the archive and each user can mark a message as read or archive it. Only the administrator can create new messages and send them directly to specific users. The other users must use the contact form, which automatically forwards the message to the administrator.
When the user is logged in, he has the possibility to add services to the shopping cart and also to remove them. On the shopping cart page all added services are listed. Here the user has the overview of the added services. The total number and the total price of the services are displayed and the user can change the quantity of the products via icons. Once the user has found everything he needs, he can order it by clicking on a button. Then he enters his address and places a binding order. An order summary is also displayed on this page. After the order there are some congratulations and a button back to the homepage.
The admin has the possibility to visit an order page and see new orders there. Just like Messenger, the order page is divided into active and archived orders. He can go to the order and see the order ID, the username of the buyer, the order number, the different items, the quantity, the price and also the address of the buyer. He can mark an order as processed and archive it if he wants.

### Distinctiveness and Complexity:  
This project is different from the project 2 commerce, because it is not necessary to create new offers. I also created the possibility to add services to the shopping cart and place an order, which is then displayed in the administrator's profile, as well as the associated order address. It also differs from Project 3 Mail in that messages are sent from the user via a contact form and are automatically forwarded to the admin. The admin responds from the message page. 
This project is much more complex than project 2 and 3. I used JS to create scrolling animations and other effects that make the website more lively and better to look at. I created 6 Django models with lots of property functions to calculate the total price or the total number of the order or other things. I wrote a lot of JS to add functionality to the page and also to add click animations to create a better user interface for example on login or messenger page. Through this course I learned to use Bootstrap and so I styled many objects of my website with Bootstrap and made my web application responsive and mobile compatible.

### Why:  
My plan is to open a small side business as a knife sharpener. With the help of this website it is possible for me to distribute business cards with the website URL on them in the neighborhood and thus collect orders online. As an administrator of the site, I can see all orders and have a structured summary of each order. I do not need a payment option on this site, as I visit the buyer using the address provided and collect their knives. Through messenger, I would like to let them know when I will pick up the knives and send them an order confirmation. Since in most cases the messages do not come from the users, I have chosen to give the reply option to the administrator alone and other requests must be made through the contact form. After sharpening, I return the knives to them and collect the money. The website is important to show the customers how I sharpen the knives, what kind of offers I have and how much the service costs.

### Files:  
The following is the file structure of the project where I added or modified. Default project files are omitted. 

/ (folder)  
-- (files)  
<pre>
/Capstone - main project folder  
  /capstone - Django main project folder  
    --settings.py - installed the app knivesharpener  
    --urls.py - added admin and knivesharpener path  
  /knivesharpener - Django knivesharpener app  
    /static\knivesharpener  
      /img - stores the images used in the webapp  
      --cart.js - loads the JS of the shopping cart functions  
      --index.js - loads the scroll animation for the index page and the fetch for the contact form  
      --mail.js - loads the message section  
      --offers.js - loads the scroll animation for the offer page  
      --orders.js - loads the order section for the admin  
      --register_login.js - creates the form animation  
      --styles_cart.css - styles the cart and the checkout page  
      --styles_offers.css - styles the offers page  
      --styles_orders.css - styles the orders page  
      --styles.css - styles all pages  
    /templates\knivesharpener - contains the templates of the app  
      --cart.html - loads the cart page  
      --checkout.html - loads the checkout page  
      --index.html - loads the index page  
      --layout.html - loads the layout, all other pages extend this one  
      --mails.html - loads the mail page  
      --offers.html - loads the offers page  
      --orders.html - loads the orders page  
      --register_login.html - loads the register_login page  
    --admin.py - the superuser can modify the added python classes via the admin site  
    --apps.py - the app knivesharpener was added  
    --models.py - 6 models with some property functions were created  
    --urls.py - all neccessary ulrpatterns were added  
    --views.py - the python backand and some APIs are handled here  
  --db.sqlite3 - the submitted data is stored in this database  
  --README.md - this file 
  </pre>

### Conclusion:
This project was a challenge for me because I think it contains complex functions. It took me a lot of time to build the website the way I imagined it. I wrote the front-end objects of the website in German, I hope that this is not a problem. All in all, this was a difficult and time-consuming project for me, but the joy was even greater when it finally worked.  
Before this course I had some experience in Python, but not in JS. I really appreciate how much I learned throughout this course and also in the final project.
Thank you for this opportunity, the course was fantastic. 

### How to run this web application:
1. Initialize the database with makemigrations and migrate.

*python manage.py makemigrations*  
*python manage.py migrate*  

2. Start the server.

*python manage.py runserver*

3. Open the web app in your browser.


