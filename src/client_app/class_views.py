from admin_app.class_views import StaffLoginView
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from client_app.views import login_fail_redirect, login_success_redirect


class UserLoginView(StaffLoginView):
    template_name = 'client_app/login.html'
    auth_class = BasicCustomAuthentication
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect
