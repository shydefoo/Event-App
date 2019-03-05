import hashlib, uuid
from app.models import UserAccount
from django.shortcuts import get_object_or_404

# def custom_authenticate(username, pw):
#
#     user = get_object_or_404(UserAccount, username=username)
#     salt = user.salt
#     pw = hash_password(pw, salt.salt.hex)
#     if pw == user.password:
#         return user
#     else:
#         return 'Invalid Password'
#
#
# def hash_password(password, salt):
#     hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
#     return hashed_password
#
# def generate_new_password(password):
#     salt = uuid.uuid4().hex
#     hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
#     return hashed_password, salt
#
# def print_password(password):
#     salt = uuid.uuid4().hex
#     hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
#     print("salt: {}, hash_password: {}".format(salt, hashed_password))


class CustomAuthenticationBase:
    def __init__(self, pw):
        self.pw = pw

    def authenticate(self):
        raise NotImplementedError

    def hash_password(self, pw, salt):
        raise NotImplementedError


class BasicCustomAuthentication(CustomAuthenticationBase):
    def __init__(self,pw, username):
        super().__init__(pw)
        self.username = username

    def authenticate(self):
        user = get_object_or_404(UserAccount, username=self.username)
        self.salt = user.salt.salt.hex
        pw = self.hash_password(self.pw, self.salt)
        if pw == user.password:
            return user
        else:
            return None

    def hash_password(self, pw, salt):
        hashed_password = hashlib.sha512(str(pw+ salt).encode('utf-8')).hexdigest()
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
        hashed_password = hashlib.sha512(str(pw+ salt).encode('utf-8')).hexdigest()
        return hashed_password

