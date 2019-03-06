from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from admin_app.forms import LoginForm
from app.utils.custom_auth.jwt_auth_methods import validate_request
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

def direct_login_page():
    return HttpResponseRedirect('/login/')


@require_http_methods(['GET'])
@validate_request(direct_login_page)
def validator_view(request):
    user = request.user
    if user.is_staff:
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/login/')

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        # render login page
        context = {'form': LoginForm}
        return render(request, 'admin_app/login.html', context=context)

    elif request.method =='POST':
        # process login details
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            auth_handler = BasicCustomAuthentication(pw, username)
            if auth_handler.authenticate():
                return HttpResponseRedirect('/home/')
            else:
                pass

@validate_request(direct_login_page)
def home(request):
    return HttpResponse('Login success')