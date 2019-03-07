from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from admin_app.forms import LoginForm
from admin_app.utils.cookies_handler import CookieHandler
from admin_app.views import login_fail_redirect, login_success_redirect
from app.models import Event
from app.utils.custom_auth.jwt_auth_methods import validate_staff_status, validate_request
from app.utils.custom_auth.password_handler import BasicStaffCustomAuthentication
from project.settings import JWT_COOKIE
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger


class StaffLoginView(View):
    form_class = LoginForm
    template_name = 'admin_app/login.html'
    auth_class = BasicStaffCustomAuthentication
    cookie_handler_class = CookieHandler
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect

    def get(self, request, *args, **kwargs):
        context = {'form': LoginForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            auth_handler = self.auth_class(pw, username)
            if auth_handler.authenticate():
                logger.debug('Authentication success')
                response = self.login_success_redirection_page()
                self.cookie_handler_class(response, JWT_COOKIE, auth_handler.token, None).set_cookie()
                return response
            else:
                logger.debug('Authentication failed')
                return self.login_fail_redirection_page(request)
        else:
            logger.debug('Invalid form')
            return self.login_fail_redirection_page(request)



class StaffHomeView(View):
    template_name = 'admin_app/home.html'

    @method_decorator(validate_request(login_fail_redirect))
    @method_decorator(validate_request(login_fail_redirect))
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        context = {
            'event_list': events
        }
        return render(request, self.template_name, context=context)
