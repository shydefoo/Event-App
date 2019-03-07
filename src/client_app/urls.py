from django.urls import path

from client_app.class_views import UserLoginView
from client_app.views import login

urlpatterns = [
    path('login/',UserLoginView.as_view(), name='client-login'),
    # path('home/', UserHomeView.as_view(), name='client-home')
]

