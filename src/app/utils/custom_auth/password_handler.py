import hashlib, uuid
from app.models import UserAccount
from django.shortcuts import get_object_or_404

def custom_authenticate(username, pw):

    user = get_object_or_404(UserAccount, username=username)
    salt = user.salt
    pw = hash_password(pw, salt.salt.hex)
    if pw == user.password:
        return user
    else:
        return 'Invalid Password'


def hash_password(password, salt):

    # salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
    return hashed_password


def print_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
    print("salt: {}, hash_password: {}".format(salt, hashed_password))



