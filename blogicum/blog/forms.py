from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment

# Получение модели пользователя из настроек Django
User = get_user_model()


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    Наследуется от UserCreationForm Django.

    Attributes:
        model (User): Модель пользователя, используемая для создания формы.
        fields (list): Поля, отображаемые в форме регистрации.
            - username (str): Имя пользователя на сайте
            - first_name (str): Имя пользователя
            - last_name (str): Фамилия пользователя
            - email (str): Электронная почта пользователя
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    Позволяет изменять базовые данные пользователя.

    Attributes:
        model (User): Модель пользователя.
        fields (list): Поля, доступные для редактирования.
            - username (str): Имя пользователя на сайте
            - first_name (str): Имя пользователя
            - last_name (str): Фамилия пользователя
            - email (str): Электронная почта пользователя
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PostForm(forms.ModelForm):
    """
    Форма создания и редактирования публикации (поста).
    Связана с моделью Post.

    Attributes:
        model (Post): Модель публикации.
        fields (list): Поля формы для публикации.
            - title (str): Заголовок публикации
            - text (str): Текст публикации
            - pub_date (datetime): Дата публикации
            - location (Location): Местоположение (ForeignKey к модели Location)
            - category (Category): Категория (ForeignKey к модели Category)
            - image (ImageField): Изображение публикации
            - is_published (bool): Статус публикации

    Relations:
        - location (ForeignKey): Связано с моделью Location.
        - category (ForeignKey): Связано с моделью Category.
        - author (User): Автор публикации (не включен в форму, устанавливается автоматически).
    """
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'location', 'category', 'image', 'is_published']


class CommentForm(forms.ModelForm):
    """
    Форма создания комментария к публикации.
    Связана с моделью Comment.

    Attributes:
        model (Comment): Модель комментария.
        fields (list): Поле формы.
            - text (str): Текст комментария (единственное поле формы)
        labels (dict): Подписи для полей формы.
            - text: 'Оставьте комментарий'

    Relations:
        - post (ForeignKey): Связано с моделью Post (не включено в форму).
        - author (User): Автор комментария (не включен в форму).
            Связано с моделью User.
    """
    class Meta:
        model = Comment
        fields = ['text',]

        labels = {'text': 'Оставьте комментарий'}