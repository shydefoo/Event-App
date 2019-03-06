from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from admin_app.forms import LoginForm, EventForm, PhotoForm
from admin_app.utils.cookies_handler import set_cookie
from app.models import Event, Photo
from app.utils.custom_auth.jwt_auth_methods import validate_request, validate_staff_status
from app.utils.custom_auth.password_handler import BasicCustomAuthentication, BasicStaffCustomAuthentication
from app.utils.serializers.serializer_response_classes import SingleEvent, SingleEventForm
from project.settings import JWT_COOKIE
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

def direct_login_page(request, *args, **kwargs):
    '''
    performs redirection to login page
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    logger.debug('redirect login page')
    return HttpResponseRedirect(reverse('login'))
    # return HttpResponse('Error Logging in', status=401)

@require_http_methods(['GET'])
@validate_request(direct_login_page)
def validator_view(request):
    '''
    Checks if user that signs in has staff status or not
    :param request:
    :return:
    '''
    user = request.user
    logger.debug(user.__dict__)
    if user.is_staff:
        logger.debug('user is_staff')
        return HttpResponseRedirect(reverse('home'))
    else:
        logger.debug('non staff')
        return HttpResponseRedirect(reverse('login'))

@require_http_methods(['GET', 'POST'])
def login(request):
    '''
    Login page
    :param request:
    :return:
    '''
    if request.method == 'GET':
        # render login page
        context = {'form': LoginForm}
        return render(request, 'admin_app/login.html', context=context)

    elif request.method =='POST':
        # process login details
        form = LoginForm(request.POST)
        logger.debug(form.errors)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            logger.debug('username: {}, pw: {}'.format(username, pw))
            auth_handler = BasicStaffCustomAuthentication(pw, username)
            if auth_handler.authenticate():
                logger.debug('Authentication success')
                response = HttpResponseRedirect(reverse('home'))
                logger.debug('token: {}'.format(auth_handler.token))
                set_cookie(response, JWT_COOKIE, auth_handler.token, None)
                return response
            else:
                logger.debug('Authentication failed')
                return direct_login_page(request)
        else:
            logger.debug('Invalid form')
            return direct_login_page(request)

@validate_request(direct_login_page)
@validate_staff_status(direct_login_page)
def home(request):
    '''
    Shows list of events
    :param request:
    :return:
    '''
    logger.debug('home view')
    # return HttpResponse('Login success')
    events = Event.objects.all()
    context = {
        'event_list': events
    }
    return render(request, 'admin_app/home.html', context=context)


@require_http_methods(['GET', 'POST'])
@validate_staff_status(direct_login_page)
def event_view(request, event_id):
    if request.method == 'GET':
        # render form with data
        event = get_object_or_404(Event, pk=event_id)
        single_event = SingleEventForm(event)
        event_form = EventForm(initial=single_event.__dict__)
        photo_form = PhotoForm()

        event_images = event.photo_set.all()

        context = {'event_id': event_id,
                   'form': event_form,
                   'photo_form': photo_form,
                   'images':event_images,
                   }

        return render(request, 'admin_app/event_view.html', context=context)

    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        f = EventForm(request.POST, instance=event)
        photo_form = PhotoForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
        if photo_form.is_valid():
            photo_form.save(commit=False)
            instance = photo_form.instance
            instance.event = get_object_or_404(Event, pk=event_id)
            instance.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            logger.error(photo_form.errors)
            return HttpResponse('error')
        # return HttpResponseRedirect(reverse('home'))

@require_http_methods(['GET', 'POST'])
@validate_staff_status(direct_login_page)
def create_event_view(request):
    if request.method == 'GET':
        context = {
            'form': EventForm
        }
        return render(request, 'admin_app/create_event_view.html', context=context)
    if request.method == 'POST':
        event = EventForm(request.POST)
        event.save()
        return HttpResponseRedirect(reverse('home'))

def photo_upload(request, event_id):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo_form.save()
            instance = photo_form.instance
            instance.event = get_object_or_404(Event, pk=event_id)
            instance.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            logger.error(photo_form.errors)
            return HttpResponse('error')

# def create_event_view(request):
#     photo_formset = modelformset_factory(Photo, form=PhotoForm, extra=3)
#     if request.method=='POST':
#         event_form = EventForm(request.POST)
#         formset = photo_formset(request.POST, request.FILES, queryset=Photo.objects.none())
#
#         if event_form.is_valid() and formset.is_valid():
#             event = event_form.save()
#
#             for form in formset.cleaned_data:
#                 if form:
#                     image = form['image']
#                     photo = Photo(image=image, event=event)
#                     photo.save()
#             return HttpResponseRedirect(reverse('home'))
#     else:
#         event_form = EventForm()
#         formset = photo_formset(queryset=Photo.objects.none())
#         context = {
#             'event_form': event_form,
#             'photo_form': formset
#         }
#         return render(request, 'admin_app/create_event_view.html', context=context)



