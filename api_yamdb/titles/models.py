from django.db import models
from django.db.models import Avg

from api_yamdb.settings import LIMIT_NAME, LIMIT_SLUG


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=LIMIT_NAME)
    slug = models.SlugField('Слаг', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=LIMIT_NAME)
    slug = models.SlugField('Слаг', max_length=LIMIT_SLUG, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=LIMIT_NAME)
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.IntegerField('Год произведения')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    @property
    def rating(self):
        return self.reviews.aggregate(Avg('score'))['score__avg']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('title', 'genre')
