from django.urls import path

from admin_app.views import validator_view, home, login

urlpatterns = [
    path('', validator_view),
    path('home/', home),
    path('login/', login),

]