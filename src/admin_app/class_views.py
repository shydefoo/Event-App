from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from admin_app.forms import LoginForm
from admin_app.utils.cookies_handler import set_cookie, CookieHandler
from admin_app.views import direct_login_page
from app.utils.custom_auth.password_handler import BasicStaffCustomAuthentication
from project.settings import JWT_COOKIE
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger


class CustomLoginView(View):
    form_class = LoginForm
    template_name = 'admin_app/login.html'
    auth_class = BasicStaffCustomAuthentication
    cookie_handler_class = CookieHandler
    redirection_page = direct_login_page

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
                response = HttpResponseRedirect(reverse('home'))
                self.cookie_handler_class(response, JWT_COOKIE, auth_handler.token, None).set_cookie()
                return response
            else:
                logger.debug('Authentication failed')
                return self.redirection_page(request)
        else:
            logger.debug('Invalid form')
            return self.redirection_page(request)
