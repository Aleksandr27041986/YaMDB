from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment
# Register your models here.


class TitleAdmin(admin.ModelAdmin):
    """
     Класс для отображения модели Title в админпанели.
    """
    list_display = ('name', 'year', 'description', 'category', 'display_genre')
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score')
    list_filter = ('score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
