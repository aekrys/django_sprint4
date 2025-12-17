from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Post, Category


def index(request):
    template = 'blog/index.html'

    posts = Post.published.all()[:5]

    context = {
        'post_list': posts
    }
    return render(request, template, context)


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)

    if not (post.is_published
            and post.pub_date <= timezone.now()
            and post.category.is_published):
        raise Http404("Пост не найден или не опубликован")

    context = {
        'post': post
    }

    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована")

    posts = Post.published.filter(category=category)

    context = {
        'category': category,
        'post_list': posts
    }

    return render(request, template, context)
