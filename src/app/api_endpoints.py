import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.serializers.event_serializer import EventSerializer
from .models import *

def get_events(request):
    events = Event.objects.all()
    event_serializer = EventSerializer(Event, events)
    json_string = event_serializer.serialize()
    response = HttpResponse(json_string, content_type="application/json")
    return response


def get_event_photos(request):
    event_id = request.GET['event_id']
    event = get_object_or_404(Event, id=event_id)
    photos = event.photo_set.all()
    
