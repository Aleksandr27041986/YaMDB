from django.core.management.base import BaseCommand

from .import_file_in_db import import_data

"""
Management-команда по загрузке данных из набора csv-файлов содержащих
экземпляры моделей Genre, Category, Title, User, Review, Comment, GenreTitle.

Пример команды:
python manage.py import_all_file

"""


data = {
    'static/data/genre.csv': 'Genre',
    'static/data/category.csv': 'Category',
    'static/data/titles.csv': 'Title',
    'static/data/users.csv': 'User',
    'static/data/genre_title.csv': 'GenreTitle',
    'static/data/review.csv': 'Review',
    'static/data/comments.csv': 'Comment'
}


class Command(BaseCommand):
    """
    Модель представления по импорту данных из csv-файлов в базу данных
    приложения.
    """
    help = 'Импорт данных из набора csv-файла в базу данных'

    def handle(self, *args, **options):
        for path, model_name in data.items():
            print(import_data(model_name, path))

