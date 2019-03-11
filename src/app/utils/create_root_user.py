import os
from app.utils.custom_auth.password_handler import BasicCustomAuthentication as BA

print('Creating root user...')
admin_username = os.environ.get('ADMIN_USERNAME')
admin_password = os.environ.get('ADMIN_PASSWORD')
user = BA.create_new_user(admin_username, admin_password, is_staff=1)
if user:
    print(user.username)
    print('Root user created')
else:
    print('Could not create user')