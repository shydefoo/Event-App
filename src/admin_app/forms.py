from django.forms import ModelForm

from app.models import UserAccount


class LoginForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'password']
