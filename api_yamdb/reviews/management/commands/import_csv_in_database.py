# Management-команда по импорту данных из csv-файлов в базу данных проекта.
# пример команды:
# python manage.py import_csv_in_database --path static/data/genre.csv --models Genre

import csv
import os

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError


from api_yamdb.settings import BASE_DIR


def read_model(model_name, path):
    """
    Функция по добавлению в базу данных экземпляров класса указанной модели.
    В качестве аргумента принимает путь до csv-файла
    и модель класса представления.
    """
    model_type = ContentType.objects.filter(model=model_name.lower()).first()
    if not model_type:
        return

    model = model_type.model_class()
    items = []
    path = os.path.join(BASE_DIR, path)
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            items.append(model(**row))

        if items:
            model.objects.bulk_create(items)


class Command(BaseCommand):
    """
    Модель представления по импорту данных из csv-файлов в базу данных
    приложения.
    """
    help = 'Импорт данных из csv-файла в базу данных'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--paths",
            dest="paths",
            nargs='+',
            help="Список путей к csv-файлу",
            type=str,
        )
        parser.add_argument(
            "--models",
            dest="models",
            nargs='+',
            help="Список названий моделей",
            type=str,
        )

    def handle(self, *args, **options):
        paths = options.get("paths")
        models = options.get("models")

        if not models:
            raise CommandError('Не указана модель представления')

        if models and paths:
            if len(models) != len(paths):
                raise CommandError('Количество путей и моделей не совпадает')

            for model_name, path in zip(models, paths):
                read_model(model_name, path)