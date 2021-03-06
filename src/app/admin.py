from django.contrib import admin

# Register your models here.
from .models import Event, Photo, UserAccount, Comment, UserSaltTable, Category


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSaltTable)
class UserSaltTable(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass