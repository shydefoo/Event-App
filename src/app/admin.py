from django.contrib import admin

# Register your models here.
from .models import Event, Photo, UserAccount

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    pass
