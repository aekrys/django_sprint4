from django.contrib import admin
from .models import Category, Post, Location


class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Category.

    Attributes:
        list_display (tuple): Поля, отображаемые на странице списка категорий.
            - title (str): Название категории
            - description (str): Описание категории
            - slug (str): URL-адрес категории (слаг)

        list_editable (tuple): Поля, доступные для редактирования прямо на странице списка.
            - description (str): Описание категории

        list_display_links (tuple): Поля-ссылки для перехода на страницу редактирования.
            - title (str): Название категории (ссылка на редактирование)

        search_fields (tuple): Поля, по которым осуществляется поиск.
            Поисковая строка отображается над списком элементов.
            Пример: search_fields = ('title', 'description', 'slug')

        list_filter (tuple): Поля для фильтрации записей.
            Фильтры отображаются справа от списка элементов.
            Пример: list_filter = ('is_published', 'created_at')
    """
    list_display = (
        'title',
        'description',
        'slug'
    )

    list_editable = (
        'description',
    )

    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Location.

    Attributes:
        list_display (tuple): Поля, отображаемые на странице списка локаций.
            - name (str): Название локации
            - is_published (bool): Статус публикации
            - created_at (datetime): Дата и время создания

        search_fields (tuple): Поля для поиска.
            Пример: search_fields = ('name',)

        list_filter (tuple): Поля для фильтрации.
            Пример: list_filter = ('is_published', 'created_at')
    """
    list_display = (
        'name',
        'is_published',
        'created_at'
    )


class PostAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Post.

    Attributes:
        list_display (tuple): Поля, отображаемые на странице списка публикаций.
            - title (str): Заголовок публикации
            - pub_date (datetime): Дата публикации
            - author (User): Автор публикации
            - location (Location): Местоположение
            - category (Category): Категория
            - is_published (bool): Статус публикации

        list_editable (tuple): Поля, доступные для редактирования в списке.
            - category (Category): Категория публикации
            - is_published (bool): Статус публикации

        search_fields (tuple): Поля для поиска публикаций.
            Рекомендуется: search_fields = ('title', 'text', 'author__username')

        list_filter (tuple): Поля для фильтрации публикаций.
            Рекомендуется: list_filter = ('is_published', 'category', 'location', 'pub_date')
    """
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )

    list_editable = (
        'category',
        'is_published',
    )

    search_fields = (
        'title',
        'text',
        'author__username',
    )

    list_filter = (
        'is_published',
        'category',
        'location',
        'pub_date',
    )


# Регистрация моделей в административной панели с соответствующими классами Admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)