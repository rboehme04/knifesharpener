from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class UserPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-Mail-Adresse',
        'type': 'text',
        'name': 'email'
        }))

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

class UserSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Neues Passwort',
        }))
    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-1',
            'placeholder': 'Neues Passwort bestätigen',
            }))

