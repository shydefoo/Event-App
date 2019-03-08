import os
SITE_IP = os.environ.get('SITE_IP')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('MYSQL_ROOT_USER')
DB_PW = os.environ.get('MYSQL_ROOT_PASSWORD')
DB_NAME = os.environ.get('MYSQL_DATABASE')
secret_key = os.environ.get('SECRET')
TIMEZONE = os.environ.get('TZ', 'Asia/Singapore')
if os.environ.get('DEBUG').upper() == 'TRUE':
    DEBUG_OR_NOT = True
else:
    DEBUG_OR_NOT = False
allowed_hosts = os.environ.get('ALLOWED_HOSTS')
_HASH_ALGO = os.environ.get('HASH_ALGO')
