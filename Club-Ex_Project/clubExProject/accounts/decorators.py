from .models import Customer, Subscription
from django.http import HttpResponse
from django.shortcuts import redirect
from .utils import has_current_subscription


# Custom Decorators and functions for verification of current users subscription status
def valid_subscription_required(view_function):
    def subscription_is_valid(request, *args, **kwargs):
        if not request.user.is_superuser:
            customer = Customer.objects.get(user = request.user)
            
            if request.user.groups.exists():
                if request.user.groups.get(name="subscriber"):
                    return view_function(request, *args, **kwargs) # return calling function
                else:
                    return redirect('renew-subscription', customer.id)
            else: 
                return redirect('renew-subscription', customer.id)
        return view_function(request, *args, **kwargs) # return calling function
    return subscription_is_valid