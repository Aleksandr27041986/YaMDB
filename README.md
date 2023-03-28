# api_yamdb
### Описание:
***


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

5. Запустить проект:

```bash
python3 manage.py runserver
```