from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import Event
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger


# Create your views here.


def login(request):
    context = {
        'form': 'form'
    }
    return render(request, 'client_app/login.html')


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


def login_fail_redirect(request):
    return HttpResponseRedirect(reverse('client-login'))


def login_success_redirect(request):
    return HttpResponseRedirect(reverse('client-home'))
