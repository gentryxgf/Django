from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from notifications.models import Notification


def my_notifications(request):
    context = dict()

    return render(request, 'my_notifications/my_notifications.html', context)


def my_notification(request, my_notification_pk):
    my_noti = get_object_or_404(Notification, pk=my_notification_pk)
    my_noti.unread = False
    my_noti.save()
    return redirect(my_noti.data['url'])


def delete_my_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))
