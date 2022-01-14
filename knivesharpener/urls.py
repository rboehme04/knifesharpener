from django.urls import path

from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserSetPasswordForm

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name='knivesharpener/password_reset.html', form_class=UserPasswordResetForm),name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='knivesharpener/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='knivesharpener/password_reset_form.html', form_class=UserSetPasswordForm), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='knivesharpener/password_reset_done.html'), name="password_reset_complete"),

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