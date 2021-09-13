from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.deletion import CASCADE
import datetime
from datetime import date
from django.urls import reverse

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=50, default='', null=True, blank=True)
    last_name = models.CharField(max_length=50, default='', null=True, blank=True)
    address_1 = models.CharField(max_length=50, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, default='', null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip_address = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    def __str__(self):
        return (self.username)

    def get_absolute_url(self):
        return reverse("view-account")

# Subscription Choices
SUBSCRIPTION_CHOICES = (
    ('ANNUAL_GYM' , 'Annual Gym Membership',),
    ('MONTHLY_GYM' , 'Monthly Gym Membership',),
    ('ANNUAL_ONLINE' , 'Annual Online Membership',),
    ('MONTHLY_ONLINE' , 'Monthly Online Membership',),
)


class Subscription(models.Model):
    subscription_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    subscription_choice = models.CharField(max_length=30, choices=SUBSCRIPTION_CHOICES,default='0')
    renewal_date = models.DateField(default=datetime.date.today)
    start_date = models.DateField(default=datetime.date.today)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateField(default=datetime.date.today)

    @property
    def is_expired(self):
        return date.today() > self.renewal_date

    @property
    def expires_today(self):
        return date.today() == self.renewal_date

    def __str__(self):
        return str(self.subscription_choice)


class Payment(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    expiry = models.DateField(default=datetime.date.today)
    cvv = models.CharField(max_length=100)
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.card_holder)

