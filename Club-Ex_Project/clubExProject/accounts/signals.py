from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer


#@receiver(post_save, sender=Profile)
def createCustomer(sender, instance, created, **kwargs):
    if created:
        user = instance
        customer = Customer.objects.create(
            user = user,
            username=user.username,
            email=user.email, 
            first_name=user.first_name,
            last_name=user.last_name
        )


def updateCustomer(sender, instance, created, **kwargs):
    customer = instance
    user = customer.user

    if created == False:
        user.first_name = customer.first_name
        user.last_name = customer.last_name
        user.username = customer.username
        user.email = customer.email
        user.save()


def deleteCustomer(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createCustomer, sender=User)
post_save.connect(updateCustomer, sender=Customer)
post_delete.connect(deleteCustomer, sender=Customer)
