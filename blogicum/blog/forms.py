from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()

# Регистрация
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# Редактирование профиля
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



# Публикация
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'location', 'category', 'image', 'is_published']


# Комментарий
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]

        labels = {'text': 'Оставьте комментарий'}
