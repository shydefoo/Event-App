from django.shortcuts import render

# Create your views here.

def login(request):
    context = {
        'form':'form'
    }
    return render(request, 'client_app/login.html')