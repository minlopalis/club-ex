from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Customer, Subscription, Payment
from .forms import CustomUserCreationForm
from .utils import SubscriptionHelper
from decimal import Decimal

# Create your views here.
def loginUser(request):
    page = 'login'
    subscription_helper = SubscriptionHelper()
    errors = {}

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if subscription_helper.has_current_subscription(user):
                login(request, user)
                return redirect('index')
            else:
                login(request, user)
                return redirect('subscription-new')
        else:
            errors = {'errors':'Username or Password is incorrect'}
    return render(request, 'login.html', errors)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print('form is valid')
            user = form.save(commit=False)
            print(user)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('subscription-new')

    context = {'page': page, 'form': form}
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def userAccount(request, pk):
    account = Customer.objects.get(id=pk)

    context = {'account': account}
    return render(request, 'club/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    customer = Customer.objects.get(request.user.profile)
    form = Customer(instance=customer)

    if request.method == 'POST':
        form = Customer(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def subscription_new(request):

    #subscription_form = SubscriptionForm
    todaysDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    context = {'start_date' : todaysDate, 'end_date': endDate}

    cost = ''
    sub_type = ''
    renewal = date.today()

    ## TODO: Add Server Side Form Validation 

    if request.method == 'POST':
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
            # Save Subscription Data
            record = Subscription.objects.create(
                subscription_choice = sub_type,
                start_date = date.today(), 
                renewal_date = renewal,
                customer_id = customer
            )
            record.save()

            # Save Payment Data
            payment_record = Payment.objects.create(
                customer_id = customer, 
                card_holder = request.POST['cardholder'],
                number = request.POST['card-number'], 
                expiry = request.POST['expiry-date'],
                cvv = request.POST['cvv'], 
                payment_amount = cost
            )
            payment_record.save()
            
            # Add user to 'subscriber' group
            group = Group.objects.get(name='subscriber')
            request.user.groups.add(group)

            return redirect('subscription-success')

    return render(request, 'subscription-new.html', context)



@login_required(login_url='login')
def subscription_success(request):
    return render(request, 'subscription-success.html')



def edit_subscription(request, pk):
    subscription_model = Subscription.objects.get(subscription_id = pk)
    payment_model = Payment
    todaysDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    
    cost = 200

    if request.method == 'POST':
        print(request.POST)
    context = { 'start_date' : todaysDate, 'end_date': endDate, 'cost': cost}
    return render(request, 'subscription-new.html', context)