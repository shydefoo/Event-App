from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from admin_app.forms import LoginForm, EventForm, PhotoForm
from admin_app.utils.cookies_handler import CookieHandler
from admin_app.views import login_fail_redirect, login_success_redirect, get_event_fail, create_event_fail, \
    create_event_success, modify_event_success
from app.models import Event
from app.utils.custom_auth.jwt_auth_methods import validate_staff_status, validate_request
from app.utils.custom_auth.password_handler import BasicStaffCustomAuthentication
from app.utils.serializers.serializer_response_classes import SingleEventForm
from project.settings import JWT_COOKIE_STAFF
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

decorators = [validate_request(login_fail_redirect), validate_staff_status(login_fail_redirect)]

class BaseView(View):
    def build_context(self, *args, **kwargs):
        pass

class StaffLoginView(BaseView):
    form_class = LoginForm
    template_name = 'admin_app/login.html'
    auth_class = BasicStaffCustomAuthentication
    cookie_handler_class = CookieHandler
    login_fail_redirection_page = login_fail_redirect
    login_success_redirection_page = login_success_redirect
    jwt_cookie_name = JWT_COOKIE_STAFF

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
                self.cookie_handler_class(response, self.jwt_cookie_name, auth_handler.token, None).set_cookie()
                return response
            else:
                logger.debug('Authentication failed')
                return self.login_fail_redirection_page()
        else:
            logger.debug('Invalid form')
            return self.login_fail_redirection_page()

    def build_context(self, form):
        context = {
            'form': form
        }
        return context

@method_decorator(decorators, name='get')
class StaffHomeView(BaseView):
    template_name = 'admin_app/home.html'

    @method_decorator(validate_request(login_fail_redirect))
    @method_decorator(validate_staff_status(login_fail_redirect))
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        context = self.build_context(events)
        return render(request, self.template_name, context=context)

    def build_context(self, events):
        context = {
            'event_list': events
        }
        return context

@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class StaffEventView(BaseView):
    template_name = 'admin_app/event_view.html'
    page_redirection_event_fail = get_event_fail
    page_redirection_event_modified_success = modify_event_success
    form_class_event = EventForm
    form_class_photo = PhotoForm
    event_form_builder = SingleEventForm


    # @method_decorator(validate_request(login_fail_redirect))
    # @method_decorator(validate_staff_status(login_fail_redirect))
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
            return self.page_redirection_event_fail()

    # @method_decorator(validate_request(login_fail_redirect))
    # @method_decorator(validate_staff_status(login_fail_redirect))
    def post(self, request, event_id, *args, **kwargs):
        try:
            event = Event.objects.get(id=event_id)
            event_form = self.form_class_event(request.POST, instance=event)
            if event_form.is_valid():
                event_form.save()
            if request.FILES.get('image',None) != None:
                photo_form = PhotoForm(request.POST, request.FILES)
                if photo_form.is_valid():
                    photo_form.save(commit=False)
                    instance = photo_form.instance
                    instance.event = Event.objects.get(id=event_id)
                    instance.save()
                else:
                    logger.error(photo_form.errors)
                    return self.page_redirection_event_fail()
            return self.page_redirection_event_modified_success(event_id)
        except Exception as e:
            return self.page_redirection_event_fail()

    def build_context(self,event_id, event_form, photo_form, event_images):
        context = {
            'event_id': event_id,
            'form': event_form,
            'photo_form': photo_form,
            'images': event_images
        }
        return context


@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class StaffCreateEventView(BaseView):
    template_name = 'admin_app/create_event_view.html'
    form_class = EventForm
    form_invalid_redirection = create_event_fail
    page_redirection_create_event_success = create_event_success

    # @method_decorator(validate_request(login_fail_redirect))
    # @method_decorator(validate_staff_status(login_fail_redirect))
    def get(self, request, *args, **kwargs):
        event_form = self.form_class()
        return render(request, self.template_name, context=self.build_context(event_form))

    # @method_decorator(validate_request(login_fail_redirect))
    # @method_decorator(validate_staff_status(login_fail_redirect))
    def post(self, request, *args, **kwargs):
        event_form = self.form_class(request.POST)
        if event_form.is_valid():
            event_form.save()
            return self.page_redirection_create_event_success()

    def build_context(self, event_form):
        context = {
            'form': event_form
        }
        return context


