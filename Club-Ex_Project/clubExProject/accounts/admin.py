from django.contrib import admin
from .models import Customer, CustomerSubscription, Subscription
# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerSubscription)
admin.site.register(Subscription)