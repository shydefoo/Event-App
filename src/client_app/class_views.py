from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from admin_app.class_views import StaffLoginView, BaseView
from app.models import Event
from app.utils.custom_auth.jwt_auth_methods import validate_request
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from client_app.views import login_fail_redirect, login_success_redirect

decorator = [validate_request(login_fail_redirect)]


class UserLoginView(StaffLoginView):
    template_name = 'client_app/login.html'
    auth_class = BasicCustomAuthentication
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect

@method_decorator(decorator, name='get')
class UserHomeView(BaseView):
    template_name = 'client_app/home.html'

    def get(self, request, *arg, **kwargs):
        events = Event.objects.all().order_by('-datetime_of_event')
        paginator = Paginator(events, 2)
        page = request.GET.get('page', 1)
        events = paginator.get_page(page)
        return render(request, self.template_name, self.build_context(events))

    def build_context(self, events, *args, **kwargs):
        context = {
            'event_list':events
        }
        return context

class UserEventView(BaseView):
    template_name = 'client_app/event_view.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('okay')
