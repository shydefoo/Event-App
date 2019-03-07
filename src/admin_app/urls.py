from django.urls import path

from admin_app.class_views import StaffLoginView, StaffHomeView, StaffEventView
from admin_app.views import validator_view, home, login, event_view, create_event_view

urlpatterns = [
    path('', validator_view, name='validator_view'),
    path('home/', StaffHomeView.as_view(), name='home'),
    path('login/', StaffLoginView.as_view(), name='login'),
    path('event/<uuid:event_id>', StaffEventView.as_view(), name='event_view'),
    path('event/create_event/', create_event_view, name='create_event'),
    # path('event/photo_upload/<uuid:event_id>', photo_upload, name='photo_upload')
]