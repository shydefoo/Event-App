from django.urls import path

from admin_app.views import validator_view, home, login, event_view, create_event_view

urlpatterns = [
    path('', validator_view, name='validator_view'),
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('event/<uuid:event_id>', event_view, name='event_view'),
    path('event/create_event/', create_event_view, name='create_event')
]