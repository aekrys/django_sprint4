from django.contrib import admin
from .models import Category, Post, Location


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)

class Category(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )

    list_editable = (
        'title',
        'description',
        'is_published',
        'created_at'
    )


class Location(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )


class Post(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )

    list_editable = (
        'category',
        'is_published',
        'created_at'
    )