from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'wallet/main.html', context)

def dashboard(request):
    context = {}
    return render(request, 'wallet/dashboard.html', context)

