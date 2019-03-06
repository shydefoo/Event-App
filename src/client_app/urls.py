from django.urls import path

from client_app.views import login

urlpatterns = [
    path('login/',login, name='client-login')
]

