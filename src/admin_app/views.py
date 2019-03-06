from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from admin_app.forms import LoginForm, EventForm
from admin_app.utils.cookies_handler import set_cookie
from app.models import Event
from app.utils.custom_auth.jwt_auth_methods import validate_request
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from app.utils.serializers.serializer_response_classes import SingleEvent
from project.settings import JWT_COOKIE
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

def direct_login_page(request, *args, **kwargs):
    logger.debug('redirect login page')
    return HttpResponseRedirect(reverse('login'))
    # return HttpResponse('Error Logging in', status=401)

@require_http_methods(['GET'])
@validate_request(direct_login_page)
def validator_view(request):
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
            auth_handler = BasicCustomAuthentication(pw, username)
            if auth_handler.authenticate():
                logger.debug('Authentication success')
                response = HttpResponseRedirect(reverse('home'))
                logger.debug('token: {}'.format(auth_handler.token))
                set_cookie(response, JWT_COOKIE, auth_handler.token, None)
                return response
            else:
                logger.debug('Authentication failed')
                pass
        else:
            logger.debug('Invalid form')
            return HttpResponseRedirect(reverse('login'))

@validate_request(direct_login_page)
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
def event_view(request, event_id):
    if request.method == 'GET':
        # render form with data
        event = get_object_or_404(Event, pk=event_id)
        single_event = SingleEvent(event)
        event_form = EventForm(initial=single_event.__dict__)
        context = {'form': event_form, 'event_id':event_id}
        return render(request, 'admin_app/event_view.html', context=context)
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        f = EventForm(request.POST, instance=event)
        f.save()
        return HttpResponseRedirect(reverse('home'))


