import uuid

from django.db import models


# Create your models here.
class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)

class Category(models.Model):
    category = models.CharField(max_length=200)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date = models.DateField(auto_created=True, auto_now_add=True)
    description = models.CharField(max_length=2000)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    participants = models.ManyToManyField(UserAccount, related_name='participants', null=True, blank=True)
    likes = models.ManyToManyField(UserAccount, related_name='likes', null=True, blank=True)



class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(auto_created=True, auto_now_add=True)


class Photo(models.Model):
    image = models.ImageField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
