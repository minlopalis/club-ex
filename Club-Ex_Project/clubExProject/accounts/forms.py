from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Payment, Subscription
from django import forms
from django.utils.translation import gettext_lazy as _
import re


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

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)



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

    def clean(self):
        super(CustomerForm, self).clean()
        self.cleaned_data['address_1']
        self.cleaned_data['address_2']
        self.cleaned_data['city']
        self.cleaned_data['zip_address']
        self.cleaned_data['country']

        email_address = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone')
 
        # email format
        email_address_format = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
        
        # check that the email_address is not blank
        if not email_address:
            self._errors['The Email Address is INVALID'] = self.error_class([
                'Email address is required'])
        
        # check email matchs the email address format
        elif not re.search(email_address_format, email_address):
                self._errors['The Email Address is INVALID'] = self.error_class([
                    'Email address is not in the correct format'])


        # phone number length format min 7 digits max 15
        phone_number_length = '^\d{7,15}$'
        # phone number numeric format 0 - 9 all positive integers 
        numeric = '^[0-9]+$'

        # check if blank
        if not phone_number:
            self._errors['The Phone Number is INVALID'] = self.error_class([
                'Phone number is required'])

        # check if entered number is numeric and strip any whitespace
        elif not re.search(numeric, str(phone_number).replace(" ", "")):
            self._errors['The Phone Number is INVALID'] = self.error_class([
                'You have entered non-numeric characters in. Please enter digits only'])

        # check if entered phone number matches the length and strip any whitespace
        elif not re.search(phone_number_length, str(phone_number).replace(" ", "")):
                self._errors['The Phone Number is INVALID'] = self.error_class([
                    'Agent phone numbers must be between 7 and 15 numbers'])
        
        # return cleaned data
        return self.cleaned_data


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
        