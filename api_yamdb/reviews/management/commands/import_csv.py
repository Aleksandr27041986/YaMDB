import csv
import os


from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import GenreTitle, Title, Genre, Category, Review, Comment


def import_genre_title(self):
    GenreTitle.objects.all().delete()
    path = os.path.join(BASE_DIR, 'static/data/genre_title.csv')
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            obj = GenreTitle.objects.create(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id'])
            )
            obj.save()

    return 'Таблица жанры произведения загружена'


def import_title(self):
    Title.objects.all().delete()
    path = os.path.join(BASE_DIR, 'static/data/titles.csv')
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            title = Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            )
            title.save()

    return 'Произведения загружены'


def import_genre(self):
    Genre.objects.all().delete()
    items = []
    path = os.path.join(BASE_DIR, 'static/data/genre.csv')
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            items.append(Genre(**row))

        if items:
            Genre.objects.bulk_create(items)
    return "Жанры загружены"


def import_category(self):
    Category.objects.all().delete()
    items = []
    path = os.path.join(BASE_DIR, 'static/data/category.csv')
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            items.append(Category(**row))

        if items:
            Category.objects.bulk_create(items)
    return 'Категории загружены'


class Command(BaseCommand):
    """
    Модель представления по импорту данных из csv-файлов в базу данных
    приложения.
    """
    help = 'Импорт данных из csv-файла в базу данных'

    def handle(self, *args, **options):
        print(import_category(self))
        print(import_genre(self))
        print(import_title(self))
        print(import_genre_title(self))


