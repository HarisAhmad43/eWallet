from django.shortcuts import render, redirect
from portfolio.views import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')

        group = Group.objects.get(name='customer')
        user.groups.add(group)
        Customer.objects.create(
            user=user,
        )

        messages.success(request, 'Account was created for ' + username)

        return redirect('login')

    context = {'form': form}
    return render(request, 'wallet/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'wallet/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def home(request):
    context = {}
    return render(request, 'wallet/home.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    context = {}
    return render(request, 'wallet/dashboard.html', context)

