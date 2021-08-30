from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from .forms import CustomUserCreationForm
# Create your views here.


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'login.html')


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
            return redirect('index')
        else:
            print('form isnt valid')
            messages.error(request, 'An error has occured during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def userAccount(request, pk):
    account = Customer.objects.get(id=pk)

    context = {'account': account}
    return render(request, 'club/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    customer = request.user.profile
    form = Customer(instance=customer)

    if request.method == 'POST':
        form = Customer(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'account.html', context)
