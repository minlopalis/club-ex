from datetime import date, datetime, timedelta
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Customer, Subscription, Payment
from .forms import CustomUserCreationForm, CustomerForm, SubscriptionForm
from .utils import has_current_subscription, renew_subscription, save_subscription

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator


# Create your views here.
def loginUser(request):
    page = 'login'

    errors = {}

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if has_current_subscription(user):
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
def view_account(request):
    customer = Customer.objects.get(user=request.user)
    subscriptions = Subscription.objects.filter(customer_id=customer)

    context = {'customer': customer, 'subscriptions': subscriptions}
    return render(request, 'account.html', context)




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

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer.phone = form.cleaned_data['phone']
            customer.email = form.cleaned_data['email']
            customer.address_1 = form.cleaned_data['address_1']
            customer.address_2 = form.cleaned_data['address_2']
            customer.city = form.cleaned_data['city']
            customer.zip_address = form.cleaned_data['zip_address']
            customer.country = form.cleaned_data['country']

            try: 
                customer.save()
                return redirect('subscription-new')
            except: 
                return redirect(request, 'customer-new.html', {'form':form})

    return render(request, 'customer-new.html', {'form': form})


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
        did_it_save = save_subscription(request)
        if did_it_save:
            return redirect('subscription-success')
        else:
            formIncomplete = "Payment Details were either entered incorrectly or are invalid please try again"
            context = {'FormIncomplete': formIncomplete, 'start_date' : todaysDate, 'end_date': endDate}
            return render(request, 'subscription-new.html', context)
    else:
        return render(request, 'subscription-new.html', context)



@login_required(login_url='login')
def subscription_success(request):
    customer = Customer.objects.get(user=request.user)
    subscription = Subscription.objects.get(customer_id=customer.id, start_date=datetime.today())
    form = SubscriptionForm(instance=subscription)
    return render(request, 'subscription-success.html', {'form': form, 'customer': customer})



def edit_subscription(request, pk):
    try:
        subscription_model = Subscription.objects.get(customer_id = pk)
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
        if request.POST['expiry-date'] >= todaysDate:
            did_it_save = renew_subscription(request, subscription_model, payment_model)
            if did_it_save:
                return redirect('subscription-success')
            else:
                formIncomplete = "Payment Details were either entered incorrectly or are invalid please try again"
                context = {'FormIncomplete': formIncomplete, 'start_date' : todaysDate, 'end_date': endDate, 'cost': cost}
                return render(request, 'subscription-new.html', context)
        else:
            formIncomplete = "Payment Details were either entered incorrectly or are invalid please try again"
            context = {'FormIncomplete': formIncomplete, 'start_date' : todaysDate, 'end_date': endDate, 'cost': cost}
            return render(request, 'subscription-new.html', context)

    context = { 'start_date' : todaysDate, 'end_date': endDate, 'cost': cost}
    return render(request, 'subscription-new.html', context)

