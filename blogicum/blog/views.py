from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from .models import Post, Category, Comment
from .forms import RegistrationForm, PostForm, CommentForm, ProfileEditForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Получение модели пользователя из настроек Django
User = get_user_model()


def registration(request):
    """
    Представление для регистрации нового пользователя.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
    Returns:
        HttpResponse: Рендерит страницу регистрации.
    """
    template = 'registration/registration_form.html'

    form = RegistrationForm()
    context = {'form': form}

    return render(request, template, context)


def profile(request, username):
    """
    Представление для отображения профиля пользователя.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        username (str): Имя пользователя, чей профиль запрашивается.

    Returns:
        HttpResponse: Рендерит страницу профиля пользователя.

    Logic:
        - Для владельца профиля отображаются ВСЕ посты (даже неопубликованные).
        - Для других пользователей отображаются только ОПУБЛИКОВАННЫЕ посты.
        - Посты аннотируются количеством комментариев.
        - Посты сортируются по дате публикации (новые первыми).
        - Используется пагинация (10 постов на страницу).
    """
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


@login_required
def edit_profile(request):
    """
    Представление для редактирования профиля пользователя.
    Доступно только аутентифицированным пользователям.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponseRedirect: Перенаправляет на профиль после успешного сохранения.
        HttpResponse: Рендерит страницу редактирования профиля.

    Logic:
        - При GET: отображает форму с текущими данными пользователя.
        - При POST: валидирует и сохраняет форму, затем перенаправляет на профиль.
    """
    template = 'blog/user.html'
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    context = {'form': form}
    return render(request, template, context)


@login_required
def create_post(request):
    """
    Представление для создания новой публикации.
    Доступно только аутентифицированным пользователям.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponseRedirect: Перенаправляет на профиль после успешного создания.
        HttpResponse: Рендерит страницу создания публикации.

    Logic:
        - При GET: отображает пустую форму.
        - При POST: валидирует форму, устанавливает автором текущего пользователя,
          сохраняет пост и перенаправляет на профиль пользователя.
    """
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


@login_required
def edit_post(request, post_id):
    """
    Представление для редактирования существующей публикации.
    Доступно только автору публикации.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        post_id (int): ID публикации для редактирования.

    Returns:
        HttpResponseRedirect: Перенаправляет на страницу поста после сохранения.
        HttpResponse: Рендерит страницу редактирования публикации.

    Security:
        - Проверяет, что текущий пользователь - автор поста.
        - Если не автор - перенаправляет на страницу поста без возможности редактирования.
    """
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


@login_required
def add_comment(request, post_id):
    """
    Представление для добавления комментария к публикации.
    Доступно только аутентифицированным пользователям.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        post_id (int): ID публикации, к которой добавляется комментарий.

    Returns:
        HttpResponseRedirect: Перенаправляет на страницу поста.

    Logic:
        - При POST: создает комментарий, связывая его с постом и текущим пользователем.
        - При GET: просто перенаправляет на страницу поста.
        - Использует commit=False для установки связей перед сохранением.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Пока не сохраняем в базу данных
            comment.post = post
            comment.author = request.user
            comment.save()  # Сохраняем в БД уже с определением, к какому посту и от какого пользователя
    return redirect('blog:post_detail', id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """
    Представление для редактирования комментария.
    Доступно только автору комментария.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        post_id (int): ID публикации, к которой относится комментарий.
        comment_id (int): ID комментария для редактирования.

    Returns:
        HttpResponseRedirect: Перенаправляет на страницу поста после сохранения.
        HttpResponse: Рендерит страницу редактирования комментария.
    """
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


@login_required
def delete_post(request, post_id):
    """
    Представление для удаления публикации.
    Доступно только автору публикации.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        post_id (int): ID публикации для удаления.

    Returns:
        HttpResponseRedirect: Перенаправляет на профиль после удаления.
        HttpResponse: Рендерит страницу подтверждения удаления (при GET).

    Security:
        - Проверяет, что текущий пользователь - автор поста.
        - Двойное подтверждение: GET показывает пост, POST удаляет его.
    """
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


@login_required
def delete_comment(request, post_id, comment_id):
    """
    Представление для удаления комментария.
    Доступно только автору комментария.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        post_id (int): ID публикации, к которой относится комментарий.
        comment_id (int): ID комментария для удаления.

    Returns:
        HttpResponseRedirect: Перенаправляет на страницу поста после удаления.
        HttpResponse: Рендерит страницу подтверждения удаления (при GET).

    Security:
        - Двойное подтверждение: GET показывает форму, POST удаляет комментарий.
    """
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
    """
    Главная страница сайта (лента публикаций).

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: Рендерит главную страницу.

    Logic:
        - Отображает только опубликованные посты (через менеджер .published).
        - Посты аннотируются количеством комментариев.
        - Сортировка по дате публикации (новые первыми).
        - Пагинация: 10 постов на страницу.
    """
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
    """
    Страница детального просмотра публикации.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        id (int): ID публикации для отображения.

    Returns:
        HttpResponse: Рендерит страницу поста.
        Http404: Если пост не найден или не доступен для просмотра.

    Security:
        - Для не-авторов проверяет, что пост опубликован,
          дата публикации наступила и категория опубликована.
        - Авторы видят свои посты всегда (даже неопубликованные).
    """
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
    """
    Страница с публикациями определенной категории.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        category_slug (str): Слаг (URL-идентификатор) категории.

    Returns:
        HttpResponse: Рендерит страницу категории.
        Http404: Если категория не найдена или не опубликована.

    Logic:
        - Проверяет, что категория опубликована.
        - Отображает только опубликованные посты в этой категории.
        - Посты аннотируются количеством комментариев.
        - Пагинация: 10 постов на страницу.
    """
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