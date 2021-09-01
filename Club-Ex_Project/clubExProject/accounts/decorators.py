from .models import Customer, Subscription
from django.http import HttpResponse
from django.shortcuts import redirect
from .utils import SubscriptionHelper


# Custom Decorators and functions for verification of current users subscription status
def valid_subscription_required(view_function):
    def subscription_is_valid(request, *args, **kwargs):
        if not request.user.is_superuser:
            customer = Customer.objects.get(user = request.user)
            customer_subscription = Subscription.objects.get(customer_id = customer.id)

            if request.user.groups.exists:
                if request.user.groups.get(name="subscriber"):
                    return view_function(request, *args, **kwargs) # return calling function
                else:
                    return redirect('renew-subscription', customer_subscription.subscription_id)
            else: 
                return redirect('renew-subscription', customer_subscription.subscription_id)
        return view_function(request, *args, **kwargs) # return calling function
    return subscription_is_valid