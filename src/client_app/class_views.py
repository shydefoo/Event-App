from django.core.paginator import Paginator
from django.shortcuts import render

from admin_app.class_views import StaffLoginView, BaseView
from app.models import Event
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
        events = Event.objects.all()
        paginator = Paginator(events, 5)
        page = request.GET.get('page', 1)
        events = paginator.get_page(page)
        return render(request, self.template_name, self.build_context(events))

    def build_context(self, events, *args, **kwargs):
        context = {
            'event_list':events
        }
        return context

