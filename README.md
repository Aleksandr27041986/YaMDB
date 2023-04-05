# api_yamdb
### Описание:
***
Проект YaMDb собирает отзывы пользователей на произведения.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Aleksandr27041986/api_final_yatube.git
```

```bash
cd api_yamdb
```

2. Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
python -m pip install --upgrade pip
```

3. Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python manage.py migrate
```
5. Запустить загрузку данных из всех сsv-файлов:

```bash
python manage.py import_all_files
```

Или загрузить самому указывая путь и модель:

```bash
python manage.py import_file_in_db --path static/data/genre.csv --models Genre
```

6. Запустить проект:

```bash
python manage.py runserver
```

### Примеры запросов:

Адрес для работы с API http://127.0.0.1:8000/api/v1/
Пример Post-запроса по адресу [titles](http://127.0.0.1:8000/api/v1/titles/)
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Полученный ответ:
```json
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}

```
Подробнее с примерами запросов и эндпоинтами можно ознакомиться в 
[документации redoc](http://127.0.0.1:8000/redoc/)
