import json

import jsonpickle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from utils.logger_class import EventsAppLogger
from utils.serializers.event_serializer import EventSerializer, EventParticipantsSerializer
from .models import *

logger = EventsAppLogger(__name__).logger

def get_events(request):
    events = Event.objects.all()
    event_serializer = EventSerializer(Event, events)
    json_string = event_serializer.serialize()
    response = HttpResponse(json_string, content_type="application/json")
    return response


def get_event_photos(request, event_id):
    logger.debug('Get event photos')
    event = get_object_or_404(Event, pk=event_id)
    photos = event.photo_set.all()
    url_list = []
    for photo in photos:
        url_list.append(photo.image.url)
    response = JsonResponse(url_list, safe=False)
    return response

def join_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        event = get_object_or_404(Event, pk=event_id)
        user = get_object_or_404(UserAccount, pk=user_id)
        event.participants.add(user)
        logger.info('{} joined event'.format(user))
        return HttpResponse('Successfully joined event', status=202)
    else:
        return HttpResponse('Get method not allowed', status=400)



def like_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        event = get_object_or_404(Event, pk=event_id)
        user = get_object_or_404(UserAccount, pk=user_id)
        event.likes.add(user)
        logger.info('{} liked event'.format(user))
        return HttpResponse('Successfully liked event', status=202)
    else:
        return HttpResponse('Get method not allowed', status=400)

def comment_on_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        comment = request.POST.get('comment')
        event = get_object_or_404(Event, pk=event_id)
        user = get_object_or_404(UserAccount, pk=user_id)
        comment = Comment(comment=comment, user=user, event=event)
        comment.save()
        return HttpResponse('Successfully commented on event', status=202)
    else:
        return HttpResponse('Get method not allowed', status=400)


def get_event_partitipants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = event.participants.all()
    json_string = EventParticipantsSerializer(participants).serialize()
    return JsonResponse(json_string, safe=False)

def get_event_likes(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    likes = event.likes.all()
