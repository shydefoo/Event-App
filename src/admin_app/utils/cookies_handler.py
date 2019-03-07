import datetime

from project import settings


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN or None)


class CookieHandler:
    def __init__(self, response, key, value, days_expire=7):
        self.response = response
        self.key = key
        self.value = value
        self.days_expire = days_expire
    def set_cookie(self):
        if self.days_expire is None:
            max_age = 365 * 24 * 60 * 60
        else:
            max_age = self.days_expire * 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")
        self.response.set_cookie(self.key, self.value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN or None)

