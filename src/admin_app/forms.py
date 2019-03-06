from django import forms

from app.models import UserAccount, Event


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput() )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['datetime_of_event', 'description', 'category','title', 'location']
        widgets = {
            'datetime_of_event' : forms.DateInput(attrs={'class':'datetime-input'}),
        }