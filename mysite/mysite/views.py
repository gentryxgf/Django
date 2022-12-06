import datetime

from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from django.core.cache import cache
from django.utils import timezone
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, \
    get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_details__read_num'))\
                        .order_by('-read_num_sum')
    return blogs[:7]

def get_hot_blogs(day):
    """
    :param day: (int)以当前日期往前的一段时间。eg. 0表示获取当天的热点博客
                1表示获取昨天的博客，7表示获取7天内的热点博客
    :return: 热点博客降序
    """
    day = int(day)
    today = timezone.now().date()
    if day==0:
        blogs = Blog.objects.filter(read_details__date=today)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_details__read_num'))\
                        .order_by('-read_num_sum')
    else:
        date = today - datetime.timedelta(days=day)
        blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
            .values('id', 'title') \
            .annotate(read_num_sum=Sum('read_details__read_num')) \
            .order_by('-read_num_sum')
    return blogs[:7]

def get_hot_blogs_cache(day, name):
    """
    :param day: int
    :param name: str
    :return: blogs
    """
    data = cache.get(name)
    if data is None:
        data = get_hot_blogs(day)
        cache.set(name, data, 3600)
    return data


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums =get_seven_days_read_data(blog_content_type)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_hot_blogs_cache(0, 'today_hot_data')
    context['yesterday_hot_data'] = get_hot_blogs_cache(1, 'yesterday_hot_data')
    context['hot_blogs_for_7_days'] = get_hot_blogs_cache(7, 'hot_blogs_for_7_days')
    # context['today_hot_data'] = get_hot_blogs(0)
    # context['yesterday_hot_data'] = get_hot_blogs(1)
    # context['hot_blogs_for_7_days'] = get_hot_blogs(7)
    # 对应read_statistic\utils\get_today_hot_data方法
    # 传入前端后对应的<li><a href="{% url 'blog_detail' hot_data.content_type.pk %}" >{{ hot_data.content_type.title }}</a>({{ hot_data.read_num }})</li>
    # context['today_hot_data'] = get_today_hot_data(blog_content_type)
    # context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    # 对应上面的get_7_days_hot_blogs方法
    # context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    return render(request, 'home.html', context)

def login(request):

    """username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})"""
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(request, username=username, password=password)
            # if user is not None:
            #     auth.login(request, user)
            #     return redirect(request.GET.get('from', reverse('home')))
            # else:
            #     login_form.add_error(None, '用户名或密码不正确')
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)