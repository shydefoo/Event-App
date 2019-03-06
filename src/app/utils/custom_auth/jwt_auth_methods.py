from functools import wraps

import jwt
from django.http import HttpResponse, JsonResponse
from requests import Response

from app.utils.custom_auth.password_handler import JWTTokenAuthentication, \
    BasicCustomAuthentication
from project import settings
from project.settings import HASH_ALGO
from utils.logger_class import EventsAppLogger

key = settings.SECRET_KEY

logger = EventsAppLogger(__name__).logger


def validate_request(redirect_func: callable):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            authorization = request.META.get('HTTP_AUTHORIZATION', None)
            if authorization is not None:
                jwt_token = authorization.split(' ')[1]
                try:
                    decoded = jwt.decode(jwt_token, key, algorithm=HASH_ALGO)
                    user_id = decoded['user_id']
                    pw = decoded['pw']  # raw or hashed password?

                    # user = get_object_or_404(UserAccount, pk=user_id)
                    # salt = user.salt.salt.hex
                    # if user.password == hash_password(pw, salt):
                    auth_handler = JWTTokenAuthentication(pw, user_id)
                    if auth_handler.authenticate():
                        logger.debug('True')
                        request.user = auth_handler.user
                        return func(request, *args, **kwargs)
                    else:
                        logger.debug('False')
                        # return HttpResponse('Invalid token', status=401)
                        # function to redirect
                        return redirect_func
                except Exception as e:
                    logger.error(str(e))
                    return HttpResponse('Error processing token', status=401)
            else:
                # return JsonResponse({'detail': 'Authentication credentials were not provided'}, status=401)
                return redirect_func
        return inner

    return decorator


def generate_token(username, pw):
    auth_handler = BasicCustomAuthentication(pw, username)
    user = auth_handler.authenticate()
    if user is not None:
        payload = {
            'user_id': user.id.hex,
            'pw': pw
        }
        token = jwt.encode(payload, key, algorithm=HASH_ALGO)
        logger.debug(token)
        return token
    else:
        return 'Incorrect credentials'
