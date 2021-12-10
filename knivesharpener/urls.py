from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("email_index", views.email_index, name="email_index"),
    path("offers", views.offers, name="offers"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path('update_listing', views.updateListing, name='update_listing'),
    path('process_cart', views.processCart, name='process_cart'),
    path('orders', views.orders, name="orders"),

    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
    path("order/<int:order_id>", views.order, name="order"),
    path("order/<str:orderbox>", views.orderbox, name="orderbox")

]