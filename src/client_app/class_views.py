from django.shortcuts import render

from admin_app.class_views import StaffLoginView, BaseView
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from client_app.views import login_fail_redirect, login_success_redirect


class UserLoginView(StaffLoginView):
    template_name = 'client_app/login.html'
    auth_class = BasicCustomAuthentication
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect


class UserHomeView(BaseView):
    template_name = 'client_app/home.html'

    def get(self, request, *arg, **kwargs):
        return render(request, self.template_name, context=self.build_context())