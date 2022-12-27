from django.contrib import admin
from .models import LikeRecord, LikeCount


@admin.register(LikeCount)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'like_num')


@admin.register(LikeRecord)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'liked_time', 'user')