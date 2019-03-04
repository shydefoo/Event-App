import uuid

from django.db import models

# Create your models here.
class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date = models.DateField()
    description = models.CharField(max_length=2000)
    title = models.CharField(max_length=200)
    participants = models.ManyToManyField(UserAccount, related_name='participants')
    likes = models.ManyToManyField(UserAccount, related_name='likes')

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)





