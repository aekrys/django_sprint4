from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class PublishedManager(models.Manager):
    """
    Менеджер для фильтрации опубликованных записей.
    Наследуется от стандартного models.Manager.

    Methods:
        get_queryset(): Возвращает отфильтрованный набор записей из базы данных (QuerySet).
            Фильтрует записи по следующим критериям:
            - is_published=True (запись опубликована)
            - category__is_published=True (категория опубликована)
            - pub_date__lte=timezone.now() (дата публикации не в будущем)
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )


class Published(models.Model):
    """
    Абстрактная модель для добавления полей публикации.
    Наследуется от models.Model.

    Attributes:
        is_published (BooleanField): Статус публикации.
            - default=True (публиковать по умолчанию)
            - verbose_name='Опубликовано'
            - help_text='Снимите галочку, чтобы скрыть публикацию.'

        created_at (DateTimeField): Дата и время создания записи.
            - auto_now_add=True (автоматически устанавливается при создании)
            - verbose_name='Добавлено'

    Meta:
        abstract = True (модель не создает таблицу в БД, используется как базовый класс для других моделей)

    """
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


# Получение модели пользователя из настроек Django
User = get_user_model()


class Category(Published):
    """
    Модель тематической категории.
    Наследуется от абстрактной модели Published.

    Attributes:
        title (CharField): Название категории.
            - max_length=256
            - verbose_name='Заголовок'

        description (TextField): Описание категории.
            - verbose_name='Описание'

        slug (SlugField): Уникальный идентификатор для URL (человекочитаемый ключ для поиска)
            - unique=True
            - verbose_name='Идентификатор'
            - help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.'

    Relations:
        - Связана с моделью Post через ForeignKey (обратная связь: post_set).
            При удалении категории: SET_NULL (посты остаются, category становится NULL).

    Managers:
        objects (models.Manager): Стандартный менеджер Django.
        published (PublishedManager): Кастомный менеджер для получения только опубликованных категорий.

    Meta:
        verbose_name='категория'
        verbose_name_plural='Категории'

    Methods:
        __str__(): Возвращает название категории (title).
    """
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
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()


class Location(Published):
    """
    Модель географической метки (местоположения).
    Наследуется от абстрактной модели Published.

    Attributes:
        name (CharField): Название места.
            - max_length=256
            - verbose_name='Название места'

    Relations:
        - Связана с моделью Post через ForeignKey (обратная связь: post_set).
            При удалении локации: SET_NULL (посты остаются, location становится NULL).

    Managers:
        objects (models.Manager): Стандартный менеджер Django.
        published (PublishedManager): Кастомный менеджер для получения только опубликованных локаций.

    Meta:
        verbose_name='местоположение'
        verbose_name_plural='Местоположения'

    Methods:
        __str__(): Возвращает название места (name).
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name

    objects = models.Manager()
    published = PublishedManager()


class Post(Published):
    """
    Модель публикации (поста).
    Наследуется от абстрактной модели Published.

    Attributes:
        title (CharField): Заголовок публикации.
            - max_length=256
            - verbose_name='Заголовок'

        text (TextField): Текст публикации.
            - verbose_name='Текст'

        pub_date (DateTimeField): Дата и время публикации.
            - verbose_name='Дата и время публикации'
            - help_text='Если установить дату и время в будущем — можно делать отложенные публикации.'

        image (ImageField): Изображение публикации.
            - upload_to='posts_images/' (путь для загрузки изображений)
            - blank=True (необязательное поле)
            - null=True (может быть NULL в БД)
            - verbose_name='Изображение'

    Relations:
        - author (ForeignKey): Автор публикации. Связано с моделью User.
            - on_delete=models.CASCADE (при удалении пользователя удаляются все его посты)
            - verbose_name='Автор публикации'

        - location (ForeignKey): Местоположение. Связано с моделью Location.
            - on_delete=models.SET_NULL (при удалении локации поле становится NULL)
            - null=True (может быть NULL)
            - blank=True (необязательное поле в формах)
            - verbose_name='Местоположение'

        - category (ForeignKey): Категория. Связано с моделью Category.
            - on_delete=models.SET_NULL (при удалении категории поле становится NULL)
            - null=True (может быть NULL)
            - verbose_name='Категория'

        - Связана с моделью Comment через ForeignKey (обратная связь: comments).
            При удалении поста: CASCADE (все комментарии удаляются).

    Managers:
        objects (models.Manager): Стандартный менеджер Django.
        published (PublishedManager): Кастомный менеджер для получения только опубликованных постов.

    Meta:
        verbose_name='публикация'
        verbose_name_plural='Публикации'

    Methods:
        __str__(): Возвращает заголовок публикации (title).
    """
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

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts_images/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()


class Comment(models.Model):
    """
    Модель комментария к публикации.

    Attributes:
        text (TextField): Текст комментария.

        created_at (DateTimeField): Дата и время создания комментария.
            - auto_now_add=True (автоматически устанавливается при создании)

    Relations:
        - post (ForeignKey): Публикация, к которой оставлен комментарий.
            Связано с моделью Post.
            - on_delete=models.CASCADE (при удалении поста удаляются все его комментарии)
            - related_name='comments' (обратная связь: post.comments.all())

        - author (ForeignKey): Автор комментария.
            Связано с моделью User.
            - on_delete=models.CASCADE (при удалении пользователя удаляются все его комментарии)

    Meta:
        ordering = ['created_at'] (сортировка по возрастанию даты создания)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
    """
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'