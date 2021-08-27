from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.deletion import CASCADE
import datetime
# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=50, null=True, blank=True)
    address_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, null=False)
    zip_address = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)


# Subscription Model
class Subscription(models.Model):
    subscription_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    subscription = models.CharField(max_length=50)
    billing_cycle_days = models.IntegerField()
    gym_access = models.BooleanField(default=False)


# Customer Subsription Model
class CustomerSubscription(models.Model):
    customer_subscription_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    auto_reccurring_subscription = models.BooleanField(default=True)