from datetime import date

import jwt
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from app.utils.custom_auth.jwt_auth_methods import validate_request, generate_token
from app.utils.custom_auth.password_handler import BasicCustomAuthentication
from project import settings
from project.settings import JWT_COOKIE_CLIENT
from utils.logger_class import EventsAppLogger
from app.utils.serializers.serializer_classes import EventSerializer, UsersSerializer, CommentsSerializer, \
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
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
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
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def join_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id', None)
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(UserAccount, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)

    participants = list(event.participants.all())
    res = {}
    res['reply'] = ''
    if user not in participants:
        event.participants.add(user)
        logger.info('{} joined event'.format(user))
        res['reply'] = 'Successfully joined event'
    else:
        res['reply'] = 'Already joined event'
    return JsonResponse(res, safe=False)

@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def leave_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id', None)
    res = {}
    res['reply'] = ''
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(UserAccount, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    participants = list(event.participants.all())
    if user in participants:
        event.participants.remove(user)
        res['reply'] = 'Left event'
    else:
        res['reply'] = 'Invalid request'
    return JsonResponse(res, safe=False)

@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def like_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id', None)
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(UserAccount, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    event.likes.add(user)
    logger.info('{} liked event'.format(user))
    res = {
        'reply':'Succesfully liked event'
    }
    return JsonResponse(res, safe=False)

@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def dislike_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id', None)
    res = {
        'reply':''
    }
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(UserAccount, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    if user in event.likes.all():
        event.likes.remove(user)
        res['reply'] = 'Succesfully disliked event'
    else:
        res['reply'] = 'Invalid request'
    return JsonResponse(res, safe=False)



@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def comment_on_event(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id', None)
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(UserAccount, pk=user_id)
    comment = request.POST.get('comment')
    event = get_object_or_404(Event, pk=event_id)
    id = uuid.uuid4()
    comment = Comment.objects.create(id=id, comment=comment, user=user, event=event)
    logger.debug("created comment: {}".format(comment))
    logger.debug('{} added a comment'.format(user))
    res = {
        'reply': 'Successfully commented on event'
    }
    return JsonResponse(res, safe=False)

@require_http_methods(['GET'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def get_event_participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = list(event.participants.all())
    json_string = UsersSerializer(Event, participants).serialize()
    return JsonResponse(json_string, safe=False)


@require_http_methods(['GET'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def get_event_likes(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    likes = list(event.likes.all())
    json_string = UsersSerializer(Event, likes).serialize()
    return JsonResponse(json_string, safe=False)


@require_http_methods(['GET'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def get_event_comments(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    comments = event.comment_set.all()
    logger.debug(comments)
    comment_serializer = CommentsSerializer(Comment, comments)
    json_string = comment_serializer.serialize()
    return JsonResponse(json_string, safe=False)


@require_http_methods(['GET'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def get_event_photos(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    images = event.photo_set.all()
    photo_serializer = PhotoSerializer(Photo, images)
    json_string = photo_serializer.serialize()
    return JsonResponse(json_string, safe=False)


@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def search_events(request):
    card_template = 'client_app/search_card.html'
    search_text = request.POST['search_text']
    logger.debug('search_text: {}'.format(search_text))
    if search_text is not '':
        events = list(Event.objects.filter(
            Q(title__icontains=search_text) | Q(category__category__icontains=search_text) | Q(
                location__icontains=search_text)))
        logger.debug(events)
        event_serializer = EventSerializer(Event, events)
        json_string = event_serializer.serialize()
        # return render(request, card_template, context=event_serializer.context)
        return JsonResponse(json_string, safe=False)
    else:
        # return HttpResponse('')
        return JsonResponse('', safe=False)


@require_http_methods(['POST'])
@validate_request(redirect_func, cookie_key=JWT_COOKIE_CLIENT)
def search_events_render(request):
    '''
    Additional endpoint to render html instead of sending json file back
    :param request:
    :return:
    '''
    card_template = 'client_app/search_card.html'
    search_text = request.POST['search_text']
    logger.debug('search_text: {}'.format(search_text))
    if search_text is not '':
        events = list(Event.objects.filter(
            Q(title__icontains=search_text) | Q(category__category__icontains=search_text) | Q(
                location__icontains=search_text)))
        logger.debug(events)
        event_serializer = EventSerializer(Event, events)
        json_string = event_serializer.serialize()
        return render(request, card_template, context=event_serializer.context)
        # return JsonResponse(json_string, safe=False)
    else:
        return HttpResponse('')
        # return JsonResponse('', safe=False)

@require_http_methods(['POST'])
@validate_request(redirect_func)
def create_user(request):
    res = {
        'reply':''
    }
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    is_staff = request.POST.get('is_staff', False)
    user = BasicCustomAuthentication.create_new_user(username, password, is_staff)
    if user == False:
        res['reply'] = 'Username already exists'
        status=202
    else:
        res['reply'] = 'User account created'
        status=200
    return JsonResponse(res, status=status)

@require_http_methods(['POST'])
@validate_request(redirect_func)
def create_category(request):
    category = request.POST.get('category', None)
    res = {
        'reply':''
    }
    if category is not None and Category.objects.filter(category=category).count() == 0:
        cat = Category(category=category)
        cat.save()
        res['reply'] = 'Sucessfully created category'
        return JsonResponse(res, status=200)
    else:
        res['reply'] = 'Category already exists or invalid request'
        return JsonResponse(res, status=202)