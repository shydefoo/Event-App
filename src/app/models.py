import uuid

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class UserSaltTable(models.Model):
    salt = models.UUIDField(default=uuid.uuid4())


class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=128)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    salt = models.OneToOneField(UserSaltTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


# class AdminUserAccount(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=128)


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category



class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date_created = models.DateField(auto_created=True, auto_now_add=True)
    datetime_of_event = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=2000)
    category = models.ManyToManyField(Category, blank=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=20, blank=True)
    participants = models.ManyToManyField(UserAccount, related_name='participants', null=True, blank=True)
    likes = models.ManyToManyField(UserAccount, related_name='likes', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('event_view', kwargs={'event_id': self.id})

    def get_user_absolute_url(self):
        return reverse('client-event-view', kwargs={'event_id':self.id})

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-datetime']




class Photo(models.Model):
    image = models.ImageField(blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.image.name