from functools import wraps

import jwt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from requests import Response

from app.utils.custom_auth.password_handler import JWTTokenAuthentication, \
    BasicCustomAuthentication
from project import settings
from project.settings import HASH_ALGO, JWT_COOKIE_STAFF
from utils.logger_class import EventsAppLogger

key = settings.SECRET_KEY

logger = EventsAppLogger(__name__).logger


# class ValidationBaseClass:
#
#     def __init__(self):
#         pass
#     def validate_request(self, *args, **kwargs):
#         raise NotImplementedError
#
#
# class ValidationHandlerClass(ValidationBaseClass):
#
#     def __init__(self, redirec_func):
#         self.redirect_func = redirec_func
#
#     def validate_request(self, redirect_func: callable):
#         '''
#         Handles request authentication using jwt
#         Checks if header contains 'authorization' or request has cookie with key 'jwt'
#         :param redirect_func:
#         :return:
#         '''
#         logger.debug('validate requests')
#
#         def decorator(func):
#             @wraps(func)
#             def inner(request, *args, **kwargs):
#                 authorization = request.META.get('HTTP_AUTHORIZATION', None)
#                 jwt_cookie = request.COOKIES.get(JWT_COOKIE_STAFF, None)
#                 logger.debug('authorization: {}, jwt_cookie: {}'.format(authorization, jwt_cookie))
#                 if authorization is not None:
#                     jwt_token = authorization.split(' ')[1]
#                 elif jwt_cookie is not None:
#                     jwt_token = str(jwt_cookie)
#                 else:
#                     return redirect_func(request, *args, **kwargs)
#
#                 try:
#                     decoded = jwt.decode(jwt_token, key, algorithm=HASH_ALGO)
#                     user_id = decoded['user_id']
#                     pw = decoded['pw']  # raw or hashed password?
#                     auth_handler = JWTTokenAuthentication(pw, user_id)
#                     if auth_handler.authenticate():
#                         logger.debug('True')
#                         request.user = auth_handler.user
#                         return func(request, *args, **kwargs)
#                     else:
#                         logger.debug('False')
#                         return redirect_func(request, *args, **kwargs)
#                 except Exception as e:
#                     logger.error(str(e))
#                     return redirect_func(request, *args, **kwargs)
#
#             return inner
#
#         return decorator
#
#     def validate_staff_status(self, redirect_func):
#         def decorator(func):
#             @wraps(func)
#             def inner(request, *args, **kwargs):
#                 user = request.user
#                 # logger.debug(user.__dict__)
#                 if user.is_staff:
#                     logger.debug('user is_staff')
#                     return func(request, *args, **kwargs)
#                 else:
#                     logger.debug('non staff')
#                     return redirect_func(request, *args, **kwargs)
#
#             return inner
#
#         return decorator
#
#     def generate_token(username, pw):
#         auth_handler = BasicCustomAuthentication(pw, username)
#         user = auth_handler.authenticate()
#         if user is not None:
#             payload = {
#                 'user_id': user.id.hex,
#                 'pw': pw
#             }
#             token = jwt.encode(payload, key, algorithm=HASH_ALGO)
#             logger.debug(token)
#             return token
#         else:
#             return 'Incorrect credentials'


def validate_request(redirect_func: callable, cookie_key=JWT_COOKIE_STAFF):
    '''
    Handles request authentication using jwt
    Checks if header contains 'authorization' or request has cookie with key 'jwt'
    :param cookie_key:
    :param redirect_func:
    :return:
    '''

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            authorization = request.META.get('HTTP_AUTHORIZATION', None)
            jwt_cookie = request.COOKIES.get(cookie_key, None)
            logger.debug('authorization: {}, jwt_cookie: {}'.format(authorization, jwt_cookie))
            if authorization is not None:
                jwt_token = authorization.split(' ')[1]
            elif jwt_cookie is not None:
                jwt_token = str(jwt_cookie)
            else:
                return redirect_func(request, *args, **kwargs)

            try:
                decoded = jwt.decode(jwt_token, key, algorithm=HASH_ALGO)
                user_id = decoded['user_id']
                pw = decoded['pw']  # raw or hashed password?
                auth_handler = JWTTokenAuthentication(pw, user_id)
                if auth_handler.authenticate():
                    logger.debug('True')
                    request.user = auth_handler.user
                    return func(request, *args, **kwargs)
                else:
                    logger.debug('False')
                    return redirect_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(str(e))
                return redirect_func(request, *args, **kwargs)

        return inner

    return decorator


def validate_staff_status(redirect_func):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user = request.user
            # logger.debug(user.__dict__)
            if user.is_staff:
                logger.debug('user is_staff')
                return func(request, *args, **kwargs)
            else:
                logger.debug('non staff')
                return redirect_func(request, *args, **kwargs)

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
        return b'Incorrect credentials'
