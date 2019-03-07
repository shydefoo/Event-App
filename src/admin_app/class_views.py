from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from admin_app.forms import LoginForm, EventForm, PhotoForm
from admin_app.utils.cookies_handler import CookieHandler
from admin_app.views import login_fail_redirect, login_success_redirect, get_event_fail
from app.models import Event
from app.utils.custom_auth.jwt_auth_methods import validate_staff_status, validate_request
from app.utils.custom_auth.password_handler import BasicStaffCustomAuthentication
from app.utils.serializers.serializer_response_classes import SingleEventForm
from project.settings import JWT_COOKIE
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

class BaseView(View):
    def build_context(self, *args, **kwargs):
        raise NotImplementedError


class StaffLoginView(BaseView):
    form_class = LoginForm
    template_name = 'admin_app/login.html'
    auth_class = BasicStaffCustomAuthentication
    cookie_handler_class = CookieHandler
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect

    def get(self, request, *args, **kwargs):
        context = self.build_context(self.form_class())
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

    def build_context(self, form):
        context = {
            'form': form
        }
        return context


class StaffHomeView(BaseView):
    template_name = 'admin_app/home.html'

    @method_decorator(validate_request(login_fail_redirect))
    @method_decorator(validate_request(login_fail_redirect))
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        context = self.build_context(events)
        return render(request, self.template_name, context=context)

    def build_context(self, events):
        context = {
            'event_list': events
        }
        return context

class StaffEventView(BaseView):
    template_name = 'admin_app/event_view.html'
    event_redirection_fail = get_event_fail
    form_class_event = EventForm
    form_class_photo = PhotoForm
    event_form_builder = SingleEventForm

    def get(self, request, event_id, *args, **kwargs):
        try:
            event = Event.objects.get(id=event_id)
            self.single_event = self.event_form_builder(event)
            event_form = self.form_class_event(initial=self.single_event.__dict__)
            photo_form = self.form_class_photo()
            event_images = event.photo_set.all()
            context = self.build_context(event_id, event_form, photo_form, event_images)
            return render(request, self.template_name, context=context)
        except Exception as e:
            logger.debug('error, '+ str(e))
            return self.event_redirection_fail()

    def build_context(self,event_id, event_form, photo_form, event_images):
        context = {
            'event_id': event_id,
            'form': event_form,
            'photo_form': photo_form,
            'images': event_images
        }
        return context
