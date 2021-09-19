from datetime import date, datetime, timedelta
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Customer, Subscription, Payment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    try:
        customer = Customer.objects.get(user=request.user)
        subscriptions = Subscription.objects.filter(customer_id=customer).order_by('-renewal_date')
        context = {'logged_user': customer, 'subscriptions': subscriptions}
    except:
        admin = User.objects.get(username=request.user)
        context = {'logged_user': admin}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def contact_us(request):
    try:
        customer = Customer.objects.get(user=request.user)
        context = {'logged_user': customer}
    except:
        admin = User.objects.get(username=request.user)
        context = {'logged_user': admin}
    return render(request, 'contact-us.html', context)


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ('index')
      
	form = ContactForm()
	return render(request, "contact.html", {'form':form})




@login_required(login_url='login')
def editAccount(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = Customer(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'account.html', context)


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CustomerForm
    
    model = Customer

    template_name = 'edit-account.html'

    context_object_name = 'account'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def form_valid(self, form):
        user = self.request.user
        data = self.request.POST
        # check user hasn't been tampered
        if data.get('user') == str(user.id):
            return super().form_valid(form)
        else:
            form.errors['Input is invalid: '] = "You can not modify your username!"
            return self.form_invalid(form)


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
    endDate = date.today().strftime('%Y-%m')

    print(endDate)

    context = {'start_date' : todaysDate, 'end_date': endDate}
    cost = ''
    sub_type = ''
    renewal = date.today()

    ## TODO: Add Server Side Form Validation 

    if request.method == 'POST':
        did_it_save = save_subscription(request)
        if did_it_save and request.POST['expiry-date'] >= endDate:
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
    subscriptions = Subscription.objects.filter(customer_id=customer.id, start_date=date.today())
    subscription = Subscription.objects.get(subscription_id=subscriptions[0].subscription_id)

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
    endDate = date.today().strftime('%Y-%m')
    cost = 200
    if request.method == 'POST':
        #print(request.POST)
        if request.POST['expiry-date'] >= endDate:
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


def cancel_subscription(request):
    try:
        customer = Customer.objects.get(user=request.user)
        subscription = Subscription.objects.filter(customer_id=customer.id, renewal_date__gt=datetime.today())
        subscription_update = Subscription.objects.get(subscription_id=subscription[0].subscription_id)
        subscription_update.renewal_date = date.today()
        subscription_update.save()
    except:
        return redirect('view-account')
    return redirect('view-account')