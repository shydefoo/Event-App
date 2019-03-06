import hashlib, uuid

import jwt

from app.models import UserAccount
from django.shortcuts import get_object_or_404

from project import settings
from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

class CustomAuthenticationBase:
    key = settings.SECRET_KEY
    hash_algo = settings.HASH_ALGO

    def __init__(self, pw):
        self.pw = pw

    def authenticate(self):
        raise NotImplementedError

    def hash_password(self, pw, salt):
        raise NotImplementedError


class BasicCustomAuthentication(CustomAuthenticationBase):
    def __init__(self, pw, username):
        super().__init__(pw)
        self.username = username

    def authenticate(self):
        user = get_object_or_404(UserAccount, username=self.username)
        self.salt = user.salt.salt.hex
        hashed_pw = self.hash_password(self.pw, self.salt)
        if hashed_pw == user.password:
            self.user = user
            self.generate_token()
            return user
        else:
            return None

    def generate_token(self):
        payload = {
            'user_id': self.user.id.hex,
            'pw': self.pw
        }
        self.token = str(jwt.encode(payload, self.key, algorithm=self.hash_algo), encoding='utf-8')

    def hash_password(self, pw, salt):
        hashed_password = hashlib.sha512(str(pw + salt).encode('utf-8')).hexdigest()
        return hashed_password

    @staticmethod
    def generate_new_password(password):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
        return hashed_password, salt


class JWTTokenAuthentication(CustomAuthenticationBase):
    def __init__(self, pw, user_id):
        super().__init__(pw)
        self.user_id = user_id

    def authenticate(self):
        user = get_object_or_404(UserAccount, pk=self.user_id)
        self.user = user
        self.salt = user.salt.salt.hex
        return user.password == self.hash_password(self.pw, self.salt)

    def hash_password(self, pw, salt):
        hashed_password = hashlib.sha512(str(pw + salt).encode('utf-8')).hexdigest()
        return hashed_password
