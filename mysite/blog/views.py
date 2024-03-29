from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 分页器，每页篇数
    page_num = request.GET.get('page', 1)  # 获取url页码参数（GET请求），如果参数不正确，则返回第一页
    page_of_blogs = paginator.get_page(page_num)  # 获取当前页码的所有blogs
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 分页列表
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # page_range = [i for i in range(current_page_num-2, current_page_num+3) if i > 0 and (i <= paginator.num_pages)]
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期分类对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = dict()
    context['blogs'] = page_of_blogs.object_list  # 当前页的所有博客列表
    context['page_of_blogs'] = page_of_blogs  # 当前页码对象
    context['page_range'] = page_range  # 分页列表
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 所有博客分类并统计各分类的数量
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()  # 获取所有blog
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

    context = dict()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    # context['comments'] = comments.order_by('-comment_time')
    # context['comment_count'] = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()
    # context['comment_form'] = CommentForm(initial=
    #                                           {
    #                                               'content_type': blog_content_type.model,
    #                                               'object_id': blog_pk,
    #                                               'reply_comment_id': 0
    #                                               })
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    """
    逻辑同blog_list页面相同
    """
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)  # 获取所有blog
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):

    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)  # 获取所有blog
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月'% (year, month)
    return render(request, 'blog/blogs_with_date.html', context)
