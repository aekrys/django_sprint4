# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


# Фильтрация записей по опубликованности
class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )


class Published(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


# Пользователь
User = get_user_model()


# Тематическая категория
class Category(Published):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name='категория'
        verbose_name_plural='Категории'

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()


# Географическая метка
class Location(Published):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name='местоположение'
        verbose_name_plural='Местоположения'

    def __str__(self):
        return self.name

    objects = models.Manager()
    published = PublishedManager()


# Публикация
class Post(Published):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    text = models.TextField(
        verbose_name='Текст'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name='публикация'
        verbose_name_plural='Публикации'

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()