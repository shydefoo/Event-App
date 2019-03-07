import jwt
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from app.utils.custom_auth.jwt_auth_methods import validate_request, generate_token
from project import settings
from utils.logger_class import EventsAppLogger
from app.utils.serializers.serializer_classes import EventSerializer, EventParticipantsSerializer, CommentsSerializer, \
    PhotoSerializer
from .models import *

logger = EventsAppLogger(__name__).logger

def redirect_func(request, *arsg, **kwargs) -> HttpResponse:
    return HttpResponse('Invalid token', status=401)

@require_http_methods(['POST'])
def get_jwt_token(request):
    key = settings.SECRET_KEY
    algo = settings.HASH_ALGO
    username = request.POST['username']
    pw = request.POST['password']
    token = generate_token(username, pw)
    return JsonResponse({'token': str(token, encoding='utf-8')})

@require_http_methods(['GET'])
@validate_request(redirect_func)
def get_events(request):
    events = list(Event.objects.all())
    event_serializer = EventSerializer(Event, events)
    json_string = event_serializer.serialize()
    response = HttpResponse(json_string, content_type="application/json")
    return response

# @require_http_methods(['GET'])
# @validate_request(redirect_func)
# def get_event_photos(request, event_id):
#     logger.debug('Get event photos')
#     event = get_object_or_404(Event, pk=event_id)
#     photos = event.photo_set.all()
#     if len(photos) == 0:
#         return HttpResponse('No Content', status=204)
#     url_list = []
#     for photo in photos:
#         url_list.append(photo.image.url)
#     response = JsonResponse(url_list, safe=False)
#     return response

@require_http_methods(['POST'])
@validate_request(redirect_func)
def join_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    event = get_object_or_404(Event, pk=event_id)
    user = get_object_or_404(UserAccount, pk=user_id)
    event.participants.add(user)
    logger.info('{} joined event'.format(user))
    return HttpResponse('Successfully joined event', status=202)

@require_http_methods(['POST'])
@validate_request(redirect_func)
def like_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    event = get_object_or_404(Event, pk=event_id)
    user = get_object_or_404(UserAccount, pk=user_id)
    event.likes.add(user)
    logger.info('{} liked event'.format(user))
    return HttpResponse('Successfully liked event', status=202)

@require_http_methods(['POST'])
@validate_request(redirect_func)
def comment_on_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    comment = request.POST.get('comment')
    event = get_object_or_404(Event, pk=event_id)
    user = get_object_or_404(UserAccount, pk=user_id)
    comment = Comment(comment=comment, user=user, event=event)
    comment.save()
    logger.debug('{} added a comment'.format(user))
    return HttpResponse('Successfully commented on event', status=202)


@require_http_methods(['GET'])
@validate_request(redirect_func)
def get_event_partitipants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = event.participants.all()
    json_string = EventParticipantsSerializer(participants).serialize()
    return JsonResponse(json_string, safe=False)

@require_http_methods(['GET'])
@validate_request(redirect_func)
def get_event_likes(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    likes = event.likes.all()

@require_http_methods(['GET'])
@validate_request(redirect_func)
def get_event_comments(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    comments = event.comment_set.all()
    logger.debug(comments)
    comment_serializer = CommentsSerializer(Comment, comments)
    json_string = comment_serializer.serialize()
    return JsonResponse(json_string, safe=False)

@require_http_methods(['GET'])
@validate_request(redirect_func)
def get_event_photos(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    images = event.photo_set.all()
    photo_serializer = PhotoSerializer(Photo, images)
    json_string = photo_serializer.serialize()
    return JsonResponse(json_string, safe=False)

@require_http_methods(['POST'])
@validate_request(redirect_func)
def search_events(request):
    card_template = 'client_app/search_card.html'
    search_text = request.POST['search_text']
    logger.debug('search_text: {}'.format(search_text))
    if search_text is not '':
        events = list(Event.objects.filter(Q(title__icontains=search_text) | Q(category__category__icontains=search_text) | Q(location__icontains=search_text)))
        logger.debug(events)
        event_serializer = EventSerializer(Event, events)
        json_string = event_serializer.serialize()
        return render(request, card_template, context=event_serializer.context)
    else:
        return HttpResponse('')


