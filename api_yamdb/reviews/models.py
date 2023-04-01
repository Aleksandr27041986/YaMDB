from django.db import models


class Category(models.Model):
    """
    Модель представления категории произведения(например фильм, книга).
    """
    objects = models.Manager()
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        """Вывод удобочитаемого наименования объекта модели."""
        return self.name


class Genre(models.Model):
    """
    Модель представления жанра произведения(например "Сказка", "Рок").
    """
    objects = models.Manager()
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = "Жанры"

    def __str__(self):
        """Вывод удобочитаемого наименования объекта модели."""
        return self.name


class Title(models.Model):
    """
    Модель представления произведения.
    """
    objects = models.Manager()
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(blank=True, verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles', db_table='reviews_genre_title',
        blank=True, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True,
        blank=True, verbose_name='Категория'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = "Произведения"

    def display_genre(self):
        """
        Создание строки со всеми жанрами произведения для отображения в
        админпанели.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Жанры'
