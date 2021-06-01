from django import forms
#from django.contrib.auth import password_validation
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm ,PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import fields
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=' Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}),help_text=password_validation)
    new_password2 = forms.CharField(label=_("Retype New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"),widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    new_password2 = forms.CharField(label=_("New password confirmation"),widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'location', 'mobile_number']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
          'email':forms.TextInput(attrs={'class':'form-control'}),
         'location':forms.TextInput(attrs={'class':'form-control'}),
         'mobile_number':forms.TextInput(attrs={'class':'form-control'})}