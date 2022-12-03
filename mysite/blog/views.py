from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType

# Create your views here.

def blog_list(request):
    blog_all_list = Blog.objects.all() #获取所有blog
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER) #分页器，每页篇数
    page_num = request.GET.get('page', 1)  # 获取url页码参数（GET请求），如果参数不正确，则返回第一页
    page_of_blogs = paginator.get_page(page_num) #获取当前页码的所有blogs
    current_page_num = page_of_blogs.number #获取当前页码
    #分页列表
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num+2, paginator.num_pages) + 1))
    #page_range = [i for i in range(current_page_num-2, current_page_num+3) if i > 0 and (i <= paginator.num_pages)]
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    context['blogs'] = page_of_blogs.object_list #当前页的所有博客列表
    context['page_of_blogs'] = page_of_blogs #当前页码对象
    context['page_range'] = page_range #分页列表
    # context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all() #所有博客分类
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):

    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    """
    逻辑同blog_list页面相同
    """
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type) #获取所有blog
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER) #分页器，每页10篇
    page_num = request.GET.get('page', 1)  # 获取url页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number #获取当前页码
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num+2, paginator.num_pages) + 1))
    #page_range = [i for i in range(current_page_num-2, current_page_num+3) if i > 0 and (i <= paginator.num_pages)]
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()

    return render_to_response('blog/blogs_with_type.html', context)
