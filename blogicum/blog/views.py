from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from .models import Post, Category, Comment
from .forms import RegistrationForm, PostForm, CommentForm, ProfileEditForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count



User = get_user_model()

# Регистрация пользователя
def registration(request):
    template = 'registration/registration_form.html'

    form = RegistrationForm()
    context = {'form': form}

    return render(request, template, context)


# Профиль
def profile(request, username):
    template = 'blog/profile.html'

    user = get_object_or_404(User, username=username)

    owner = request.user == user
    if owner == True:
        posts = Post.objects.filter(author=user)
    else:
        posts = Post.published.filter(author=user)

    posts =  posts.annotate(comment_count=Count('comments')).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user,
        'page_obj': page_obj,
    }

    return render(request, template, context)


# Редактирование профиля
@login_required
def edit_profile(request):
    template = 'blog/user.html'

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    context = {'form': form}
    return render(request, template, context)


# Создание публикации
@login_required
def create_post(request):
    template = 'blog/create.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    context = {'form': form}

    return render(request, template, context)


# Редактирование публикации
@login_required
def edit_post(request, post_id):
    template = 'blog/create.html'

    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = PostForm(instance=post)

    context = {'form': form}

    return render(request, template, context)


# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Пока не сохраняем в базу данных
            comment.post = post
            comment.author = request.user
            comment.save()  # Сохраняем в БД уже с определением, к какому посту и от какого пользователя
    return redirect('blog:post_detail', id=post_id)


# Редактирование комментария
@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/comment.html'

    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form,
               'comment': comment}

    return render(request, template, context)


# Удаление публикации
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'GET':
        template = 'blog/detail.html'

        context = {
            'post': post,
        }

        return render(request, template, context)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)


# Удаление комментария
@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'GET':
        template = 'blog/comment.html'
        context = {
            'comment': comment,
            'post': post,
        }

        return render(request, template, context)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)






def index(request):
    template = 'blog/index.html'

    posts = Post.published.annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'

    post = get_object_or_404(Post, pk=id)

    is_author = request.user.is_authenticated and request.user == post.author

    if not is_author and not (
            post.is_published
            and post.pub_date <= timezone.now()
            and post.category.is_published):
        raise Http404("Пост не найден или не опубликован")

    comments = post.comments.all()
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована")

    posts = Post.published.filter(category=category).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }

    return render(request, template, context)
