from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH


class User(AbstractUser):
    pass

class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(minuits=0)
            return val.isoformat()
        return ''

class Email(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField("User", related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = CustomDateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y"),
            "read": self.read,
            "archived": self.archived
        }
    
    def serialize_email(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }

class Listing(models.Model):
    item_title = models.CharField(max_length=64, blank=False)
    item_description = models.TextField(max_length=64, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    image_url = models.URLField(blank=True)
    item_buyer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='items_bought')
    cart_list = models.ManyToManyField(User, blank=True, related_name="cart")
    animation_header = models.CharField(max_length=64, blank=True)
    animation_image = models.CharField(max_length=64, blank=True)

class Cart(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='user_cart')
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    cart_id = models.CharField(max_length=200, null=True)
    archived = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cart_id)
    
    @property
    def total_cart_price(self):
        cartitems = self.cartitem_set.all()
        total = sum([listing.total_price for listing in cartitems])
        return total
    
    @property
    def total_cart_listings(self):
        cartitems = self.cartitem_set.all()
        total = sum([listing.quantity for listing in cartitems])
        return total

    def serialize_order(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "cart_id": self.cart_id,
            "date_ordered": self.date_ordered.strftime("%b %d %Y, %I:%M %p"),
            "processed": self.processed,
            "archived": self.archived,
            "total_price": self.total_cart_price,
            "total_amount": self.total_cart_listings,
            "listings": [cartitem.listing_item.item_title for cartitem in self.cartitem_set.all()],
            "quantity": [cartitem.quantity for cartitem in self.cartitem_set.all()],
            "price": [cartitem.listing_item.price for cartitem in self.cartitem_set.all()],
            "total_price_listing": [cartitem.total_price for cartitem in self.cartitem_set.all()],
            "address_name": [cartitem.user_name for cartitem in self.adress_set.all()],
            "address_address": [cartitem.address for cartitem in self.adress_set.all()],
            "address_zipcode": [cartitem.zipcode for cartitem in self.adress_set.all()],
            "address_city": [cartitem.city for cartitem in self.adress_set.all()],
        }

class CartItem(models.Model):
    listing_item = models.ForeignKey(Listing, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        total = self.listing_item.price * self.quantity
        return total

class Adress(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='user_cartitem')
    user_name = models.CharField(max_length=200, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adress: {self.address}"

