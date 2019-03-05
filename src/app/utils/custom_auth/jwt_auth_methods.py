from functools import wraps
import jwt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from app.models import UserAccount
from project import settings
from project.settings import HASH_ALGO
from utils.logger_class import EventsAppLogger

key = settings.SECRET_KEY
logger = EventsAppLogger(__name__).logger

def validate_request():
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            authorization = request.META.get('HTTP_AUTHORIZATION', None)
            if authorization is not None:
                jwt_token = authorization.split(' ')[1]
                try:
                    decoded = jwt.decode(jwt_token, key, algorithm=HASH_ALGO)
                    user_id = decoded['user_id']
                    pw = decoded['pw']
                    user = get_object_or_404(UserAccount, pk=user_id)
                    if user.password == pw:
                        logger.debug('True')
                        return func(request, *args, **kwargs)
                    else:
                        logger.debug('False')
                        return HttpResponse('Invalid token')
                except Exception as e:
                    logger.error(str(e))
                    return HttpResponse('Error processing token', status=401)
            else:
                return JsonResponse({'detail':'Authentication credentials were not provided'}, status=401)
        return inner
    return decorator



