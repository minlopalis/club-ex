from .models import Customer, Subscription
from datetime import datetime

class SubscriptionHelper():
    
    def has_current_subscription(request, user):
        if not user.is_superuser:
            customer = Customer.objects.get(user=user.id)
            customer_subscriptions = Subscription.objects.filter(
                customer_id = customer.id, 
                renewal_date__gte=datetime.now().date()
                )
            return customer_subscriptions.count() > 0
    
