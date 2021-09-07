from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Payment, Subscription
from django import forms
from django.utils.translation import gettext_lazy as _

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
        error_messages = {
            'first_name': {'required': 'First name is required'},
            'last_name': {'required': 'First name is required'},
            'email': {'required': 'Email address is required'},
            'username': {'required': 'Username is required'},
            'password1': {'required': 'Password is required'},
            'password2': {'required': 'Repeated Password is required'},
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'black-text validate'})
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['username'].required = True
            self.fields['password1'].required = True
            self.fields['password2'].required = True



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'country', 'zip_address', 'email', 'phone', 'user']
        help_texts = {}
        error_messages = {
            'first_name': {'required': 'First name is required'},
            'last_name': {'required': 'First name is required'},
            'address_1': {'required': 'Address Line 1 is required'},
            'city': {'required': 'City is required'},
            'country': {'required': 'Country is required'},
            'email': {'required': 'Email is required'},
            'phone': {'required': 'Phone number is requried'},
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['address_1'].required = True
        self.fields['city'].required = True
        self.fields['country'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True


        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'black-text validate'})




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


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['subscription_choice', 'renewal_date', 'start_date', 'customer_id', 'created_date']
    
    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        