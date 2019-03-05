from functools import wraps
import jwt
from django.http import HttpResponse
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
            jwt_token = request.META['jwt']
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
        return inner
    return decorator



