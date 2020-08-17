from django.shortcuts import render

# Create your views here.
def register(request):
    context = {}
    return render(request, 'wallet/register.html', context)

def login(request):
    context = {}
    return render(request, 'wallet/login.html', context)


def home(request):
    context = {}
    return render(request, 'wallet/home.html', context)

def dashboard(request):
    context = {}
    return render(request, 'wallet/dashboard.html', context)

