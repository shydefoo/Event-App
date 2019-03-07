from django.conf.urls import url
from django.urls import path

from client_app.class_views import UserLoginView, UserHomeView
from client_app.views import login

urlpatterns = [
    path('login/',UserLoginView.as_view(), name='client-login'),
    url(r'^home/', UserHomeView.as_view(), name='client-home')
]

