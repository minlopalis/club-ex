from django.contrib.auth.models import Group
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from .models import Customer, Payment, Subscription
from datetime import date, datetime, timedelta


def has_current_subscription(user):
    if not user.is_superuser:
        customer = Customer.objects.get(user=user.id)
        customer_subscriptions = Subscription.objects.filter(
            customer_id = customer.id, 
            renewal_date__gte=datetime.now().date()
            )
        if not customer_subscriptions.count() > 0:
            group = Group.objects.get(name='subscriber') 
            user.groups.remove(group)
        return customer_subscriptions.count() > 0


def save_subscription(request):
    customer = Customer.objects.get(user=request.user)
    subscription = request.POST['sub-select']
    did_it_save_payment = False
    did_it_save_subscription = False
    if subscription == '1':
        sub_type = 'MONTHLY_ONLINE'
        renewal = date.today() + timedelta(days=30)
        cost = 10.00
    elif subscription == '2':
        sub_type = 'ANNUAL_ONLINE'
        cost = 100.00
        renewal = date.today() + timedelta(days=365)
    elif subscription == '3': 
        sub_type = 'MONTHLY_GYM'
        cost = 20.00
        renewal = date.today() + timedelta(days=30)
    elif subscription == '4':
        sub_type = 'ANNUAL_GYM'
        cost = 200.00
        renewal = date.today() + timedelta(days=365)
    else: 
        cost = 0 

    if cost != 0:
        try:
            # Save Subscription Data
            record = Subscription.objects.create(
                subscription_choice = sub_type,
                start_date = date.today(), 
                renewal_date = renewal,
                customer_id = customer
            )
            record.save()
            did_it_save_subscription = True
        except:
            did_it_save_subscription = False
        try:
            # Save Payment Data
            payment_record = Payment.objects.create(
                customer_id = customer, 
                card_holder = request.POST['cardholder'],
                number = request.POST['card-number'], 
                expiry = request.POST['expiry-date']+'-01',
                cvv = request.POST['cvv'], 
                payment_amount = cost
            )
            payment_record.save()
            did_it_save_payment = True
        except:
            did_it_save_payment = False
        did_it_save = False
        if did_it_save_payment & did_it_save_subscription:
            # Add user to 'subscriber' group
            group = Group.objects.get(name='subscriber')
            request.user.groups.add(group)
            did_it_save = True
    return did_it_save


def renew_subscription(request, subscription_obj, payment_obj):
    did_it_save_payment = False
    did_it_save_subscription = False
    customer = Customer.objects.get(user=request.user)
    subscription = request.POST['sub-select']
    if subscription == '1':
        sub_type = 'MONTHLY_ONLINE'
        renewal = date.today() + timedelta(days=30)
        cost = 10.00
    elif subscription == '2':
        sub_type = 'ANNUAL_ONLINE'
        cost = 100.00
        renewal = date.today() + timedelta(days=365)
    elif subscription == '3': 
        sub_type = 'MONTHLY_GYM'
        cost = 20.00
        renewal = date.today() + timedelta(days=30)
    elif subscription == '4':
        sub_type = 'ANNUAL_GYM'
        cost = 200.00
        renewal = date.today() + timedelta(days=365)
    else: 
        cost = 0 
    if cost != 0:
        try:
            # Save Updated Subscription Data
            subscription_obj.subscription_choice = sub_type
            subscription_obj.start_date = date.today()
            subscription_obj.renewal_date = renewal
            subscription_obj.save()
            did_it_save_subscription = True
        except:
            did_it_save_subscription = False

        try:
            # Save Updated Payment Data
            payment_obj.card_holder = request.POST['cardholder']
            payment_obj.number = request.POST['card-number'] 
            payment_obj.expiry = request.POST['expiry-date']+'-01'
            payment_obj.cvv = request.POST['cvv']
            payment_obj.payment_amount = cost
            payment_obj.save()
            did_it_save_payment = True
        except:
            did_it_save_payment = False
        
        
        did_it_save = False
        # Add user to 'subscriber' group
        if did_it_save_payment & did_it_save_subscription:
            group = Group.objects.get(name='subscriber')
            request.user.groups.add(group)
            did_it_save = True

    return did_it_save
