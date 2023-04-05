from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


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
        Genre, related_name='titles', through='GenreTitle',
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


class Review(models.Model):
    """
    Модель отзыва.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому относится отзыв'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Текст',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name="Оценка",
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]


class Comment(models.Model):
    """
    Модель комментария к отзыву.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Комментарий',
        help_text='Введите ваш комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария')

    class Meta:
        ordering = ('-pub_date',)


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
