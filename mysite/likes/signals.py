from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify
from django.db.models.signals import post_save
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notification_likes(sender, instance, **kwargs):
    if instance.content_type.model == 'blog':
        blog = instance.content_object
        verb = '{0} 点赞了你的 《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
    elif instance.content_type.model == 'comment':
        comment = instance.content_object
        verb = '{0} 点赞了你的回复“{1}”'.format(instance.user.get_nickname_or_username(), strip_tags(comment.text))
    recipient = instance.content_object.get_user()
    # 发送消息
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance)
