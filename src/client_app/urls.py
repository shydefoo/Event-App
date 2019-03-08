from django.conf.urls import url
from django.urls import path

from client_app.class_views import UserLoginView, UserHomeView, UserEventView
from client_app.views import login

urlpatterns = [
    path('', UserLoginView.as_view()),
    path('login/',UserLoginView.as_view(), name='client-login'),
    url(r'^home/', UserHomeView.as_view(), name='client-home'),
    path('event_view/<uuid:event_id>', UserEventView.as_view(), name='client-event-view'),
]

