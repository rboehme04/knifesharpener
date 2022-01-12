from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .utils import render_to_pdf, save_entry, delete_entry
from django.core.files import File
from . import utils

from .models import User, Email, Listing, Cart, CartItem, Adress


def index(request):
    
    if request.user.is_authenticated:
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False)
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        if request.user.username == 'admin':
            orders = Cart.objects.filter(archived=False, processed=False, completed=True)
            total = emails.count() + cart.total_cart_listings + orders.count()
        else:
            total = emails.count() + cart.total_cart_listings
            orders = []
        context = {'cart': cart, 'emails': emails, 'animation_title': 'index', 'total': total, 'orders': orders}
        return render(request, "knivesharpener/index.html", context)
    else: 
        emails = ''
        cart = ''

    return render(request, "knivesharpener/index.html", {
        'animation_title': 'index',
        'emails': emails,
        'cart': cart
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "knivesharpener/register_login.html", {
                "message": "Passwords must match.",
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "knivesharpener/register_login.html", {
                "message": "Username already taken.",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "knivesharpener/register_login.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "knivesharpener/register_login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "knivesharpener/register_login.html",{
            'animation_title': 'login'
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def email_index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False)
        if request.user.username == 'admin':
            orders = Cart.objects.filter(archived=False, processed=False, completed=True)
            total = emails.count() + cart.total_cart_listings + orders.count()
        else:
            total = emails.count() + cart.total_cart_listings
            orders = []
        return render(request, "knivesharpener/mails.html", {
            'emails': emails,
            'cart': cart,
            'total': total,
            'orders': orders
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def compose(request):

    
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email
    subject = data.get("subject", "")
    if subject == "":
        message = 'Betreff ist erforderlich.'
        return JsonResponse({'message': message})
    body = data.get("body", "")
    if body == "":
        message = "Inhalt ist erforderlich."
        return JsonResponse({'message': message})

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    message = "Anfrage erfolgreich gesendet."
    return JsonResponse({'message': message})

  

@login_required
def mailbox(request, mailbox):
    
    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=False
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    if request.user == 'admin':
        return JsonResponse({'user': 'admin'})

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize_email())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def offers(request):

    offers = Listing.objects.all()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        listings = cart.cartitem_set.all()
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False)  
        if request.user.username == 'admin':
            orders = Cart.objects.filter(archived=False, processed=False, completed=True)
            total = emails.count() + cart.total_cart_listings + orders.count()
        else:
            total = emails.count() + cart.total_cart_listings
            orders = []
    else:
        listings = []
        cart = {'total_cart_price': 0, 'total_cart_listings': 0}
        emails = []
        total = []
        orders = []

    context = {'offers': offers, 'listings': listings, 'cart': cart, 'emails': emails, 'total': total, 'orders': orders}
    return render(request, "knivesharpener/offers.html", context)

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        listings = cart.cartitem_set.all()
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False) 
        if request.user.username == 'admin':
            orders = Cart.objects.filter(archived=False, processed=False, completed=True)
            total = emails.count() + cart.total_cart_listings + orders.count()
        else:
            total = emails.count() + cart.total_cart_listings
            orders = []
    else:
        listings = []
        cart = {'total_cart_price': 0, 'total_cart_listings': 0}
        emails = []
        total = []
        orders = []
    context = {'listings': listings, 'cart': cart, 'emails': emails, 'total': total, 'orders': orders}
    return render(request, "knivesharpener/cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        listings = cart.cartitem_set.all()
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False)
        if request.user.username == 'admin':
            orders = Cart.objects.filter(archived=False, processed=False, completed=True)
            total = emails.count() + cart.total_cart_listings + orders.count()
        else:
            total = emails.count() + cart.total_cart_listings
            orders = []
    else:
        listings = []
        cart = {'total_cart_price': 0, 'total_cart_listings': 0}
        emails = []

    context = {'listings': listings, 'cart': cart, 'emails': emails, 'total': total, 'orders': orders}
    return render(request, "knivesharpener/checkout.html", context)

def updateListing(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        listingId = data['listingId']
        action = data['action']

        print('Action: ', action)
        print('ListingId: ', listingId)

        user = request.user
        listing = Listing.objects.get(id=listingId)
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

        cartItem, created = CartItem.objects.get_or_create(cart=cart, listing_item=listing)

        if action == 'add':
            cartItem.quantity = (cartItem.quantity + 1)
        elif action == 'remove':
            cartItem.quantity = (cartItem.quantity - 1)

        cartItem.save()

        if cartItem.quantity <= 0:
            cartItem.delete()

        return JsonResponse('Item was added', safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))

def processCart(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        total = float(data['nameform']['total'])
        emailadress = data['nameform']['email']
        cart.cart_id = transaction_id

        if total == float(cart.total_cart_price):
            cart.completed = True
        cart.save()

        Adress.objects.create(
            user = request.user,
            user_name = data['nameform']['user_name'],
            cart = cart,
            address = data['addressform']['address'],
            zipcode = data['addressform']['zipcode'],
            city = data['addressform']['city'],
        )

        order = Cart.objects.get(cart_id = transaction_id)

        render_to_pdf("knivesharpener/orderconfirmation.html", {'orders': order.serialize_order()}, transaction_id)

        html_content = render_to_string("knivesharpener/orderconfirmation_html.html")
        text_content = strip_tags(html_content)


        email = EmailMultiAlternatives(
            #subject
            'Bestellbestätigung',
            #content
            text_content,
            #from email
            settings.EMAIL_HOST_USER,
            #rec list
            [emailadress]
        )
        email.attach_alternative(html_content, "text/html")
        email.attach_file(f'knivesharpener/pdf/{transaction_id}.pdf', "application/pdf")
        email.send()

    return JsonResponse('Payment complete', safe=False)

def orders(request):
    if request.user.username == 'admin':
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        listings = cart.cartitem_set.all()
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False, read=False)
        orders = Cart.objects.filter(archived=False, processed=False, completed=True)
        total = emails.count() + cart.total_cart_listings + orders.count()
        return render(request, "knivesharpener/orders.html", {
            'orders': Cart.objects.filter(archived=False),
            'emails': emails,
            'cart': cart,
            'total': total,
            'orders': orders
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def orderbox(request, orderbox):
    
    # Filter emails returned based on mailbox
    if orderbox == "inbox":
        orders = Cart.objects.filter(archived=False, completed=True)
    elif orderbox == "archive":
        orders = Cart.objects.filter(archived=True, completed=True)
    else:
        return JsonResponse({"error": "Invalid orderbox."}, status=400)


    # Return emails in reverse chronologial order
    orders = orders.order_by("-date_ordered").all()
    return JsonResponse([order.serialize_order() for order in orders], safe=False)

def order(request, order_id):

    # Query for requested email
    try:
        order = Cart.objects.get(pk=order_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(order.serialize_order())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("processed") is not None:
            order.processed = data["processed"]
        if data.get("archived") is not None:
            order.archived = data["archived"]
        order.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)