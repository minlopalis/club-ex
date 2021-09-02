from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Payment, Subscription
from django import forms
from datetime import date
from django.utils.translation import gettext_lazy as _
from accounts import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email':'Email',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'blue-text'})


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'country', 'zip_address', 'email', 'phone', 'user']
        help_texts = {
            'first_name': _('Enter your given name?'),
            'last_name': _('Enter your surname'),
            'address_1': _('Enter the first line of your address'), 
            'address_2': _('Enter the second line of your address, often this is a suburb'),
            'city': _('Enter the city or town'),
            'country': _('Enter the country'),
            'zip_address':_('Enter your zip or postal code'),
            'email': _('Enter your email address'),
            'phone': _('Enter your phone number')
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'black-text'})



    

# Subscription Choices
SUBSCRIPTION_CHOICES = (
    ('ANNUAL_GYM' , 'Annual Gym Membership',),
    ('MONTHLY_GYM' , 'Monthly Gym Membership',),
    ('ANNUAL_ONLINE' , 'Annual Online Membership',),
    ('MONTHLY_ONLINE' , 'Monthly Online Membership',),
)
# AutoRecuring Choices
AUTORECURING_CHOICES = (
    ('YES', 'Yes'),
    ('NO', 'No'),
)


# class SubscriptionForm(forms.Form):
#     renewal_date = forms.DateField(help_text="This Will be the Next payment date and will update automatically", widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
#     start_date = forms.DateField(help_text="This Will be the start date of your subscription", widget=forms.DateInput(attrs={'class': 'datepicker1', 'type': 'date'}))
#     subscritpion_choice = forms.CharField(label="Select Subscription",widget=forms.Select(choices=SUBSCRIPTION_CHOICES, attrs ={'id':"subscription-choices"}) )
#     autorecurring_choice = forms.CharField(label="Automatically Recur Subscription",widget=forms.Select(choices=AUTORECURING_CHOICES,attrs={'id':"autorecurring-choices"}) )
#     cost =  forms.CharField(label="Subscription Cost", max_length=10)