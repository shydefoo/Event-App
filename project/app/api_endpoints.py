from django.http import HttpResponse

from project.utils.serializers.event_serializer import EventSerializer
from .models import *

def get_events(request):
    events = Event.all()
    event_serializer = EventSerializer(events)
    json_string = event_serializer.serialize()
    response = HttpResponse(json_string, content_type="application/json")
    return response
