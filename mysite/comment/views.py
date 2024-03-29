from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
from notifications.signals import notify


def update_comment(request):
    """referer = request.META.get('HTTP_REFERER', reverse('home'))

    #数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})

    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})
    #检查通过
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)"""
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        """
        .signals信号发送器
        if comment.reply_to is None:
            #是评论
            recipient = comment.content_object.get_user()
            if comment.content_type.model == 'blog':
                blog = comment.content_object
                verb = '{0} 评论了你的 《{1}》'.format(comment.user.get_nickname_or_username(), blog.title)
            else:
                raise Exception('Unknow comment object type')
        else:
            #是回复
            recipient = comment.reply_to
            verb = '{0} 回复了你的评论“{1}”'.format(comment.user.get_nickname_or_username(), strip_tags(comment.parent.text))
        #发送消息
        notify.send(comment.user, recipient=recipient, verb=verb, action_object=comment)
        """

        # 发送邮件
        # 信号发送器重构
        # comment.send_mail()

        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)