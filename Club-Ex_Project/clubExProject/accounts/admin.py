from django.contrib import admin
from .models import Customer, Subscription, Payment
# Register your models here.
admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Payment)
