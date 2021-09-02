from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Customer, Subscription, Payment
from .forms import CustomUserCreationForm, CustomerForm
from .utils import SubscriptionHelper, renew_subscription, save_subscription
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
            return redirect('customer-new')

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
def customer_new(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    context = {'form': form}

    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        city = request.POST['city']
        zip_address = request.POST['zip_address']
        country = request.POST['country']

        customer.phone = phone
        customer.email = email
        customer.address_1 = address_1
        customer.address_2 = address_2
        customer.city = city
        customer.zip_address = zip_address
        customer.country = country
        
        try: 
            customer.save()
            return redirect('subscription-new')
        except: 
            return redirect(request, 'customer-new.html', context)

    return render(request, 'customer-new.html', context)


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
        save_subscription(request)
        return redirect('subscription-success')
    else:
        return render(request, 'subscription-new.html', context)



@login_required(login_url='login')
def subscription_success(request):
    return render(request, 'subscription-success.html')



def edit_subscription(request, pk):
    try:
        subscription_model = Subscription.objects.get(customer_id = pk)
        print("INITIAL SUBSCRIPTION_TYPE: ", type(subscription_model))
    except:
        return redirect('subscription-new')

    try:
        customer = Customer.objects.get(id = pk)
        payment_model = Payment.objects.get(customer_id = customer)
    except:
        return redirect('subscription-new')
    
    todaysDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    
    cost = 200
    print(subscription_model)
    if request.method == 'POST':
        #print(request.POST)
        renew_subscription(request, subscription_model, payment_model)
        return redirect('subscription-success')

        

    context = { 'start_date' : todaysDate, 'end_date': endDate, 'cost': cost}
    return render(request, 'subscription-new.html', context)

