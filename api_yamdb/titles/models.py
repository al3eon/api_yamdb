from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser


class Genre(models.Model):
    """Модель жанра.

    Атрибуты:
    name(CharField): Название категории(макс. 256 символов)
    slug(SlugField): Слаг(макс. 50 символов)
    """

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    class Meta:
        """Мета-настройки отображения модели Genre в админке и запросах."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """
        Возвращает название жанра.

        Для строкового представления объекта Genre.
        """
        return self.name


class Category(models.Model):
    """Модель категории.

    Атрибуты:
    name(CharField): Название категории(макс. 256 символов)
    slug(SlugField): Слаг(макс. 50 символов)
    """

    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        """Мета-настройки отображения модели Category в админке и запросах."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Возвращает название категории.

        Для строкового представления объекта Category.
        """
        return self.name


class Title(models.Model):
    """Модель произведения (книга, фильм, музыка и т.д.).

    Атрибуты:
        name(CharField): Название произведения (макс. 128 символов)
        description(TextField): Подробное описание (может быть пустым)
        genre(ForeignKey): Связь с жанром. При удалении жанра становится NULL.
        year(DateField): Дата выпуска произведения
        category(ForeignKey): Связь с категорией. При удалении становится NULL.
    """

    name = models.CharField('Название произведения', max_length=256)
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='titles',
        verbose_name='Жанр'
    )
    year = models.IntegerField('Год произведения')
    category = models.ForeignKey(
        Category, related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    class Meta:
        """Мета-настройки отображения модели Title в админке и запросах."""

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    #@property
    #def rating(self):
     #   return self.reviews.aggregate(Avg('score'))['score__avg']

    def __str__(self):
        """
        Возвращает название произведения.

        Для строкового представления объекта Title.
        """
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'genre')
