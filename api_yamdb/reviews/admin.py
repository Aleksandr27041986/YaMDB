from django.contrib import admin

from .models import Category, Genre, Title
# Register your models here.


class TitleAdmin(admin.ModelAdmin):
    """
     Класс для отображения модели Title в админпанели.
    """
    list_display = ('name', 'year', 'description', 'category', 'display_genre')
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
