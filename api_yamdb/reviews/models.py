from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import LIMIT_NAME, LIMIT_SLUG, MAX_SCORE, MIN_SCORE
from .validators import year_validator


class GenreCategoryBaseModel(models.Model):
    name = models.CharField('Название', unique=True, max_length=LIMIT_NAME)
    slug = models.SlugField('Слаг', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'{self.__class__.__name__} '


class Genre(GenreCategoryBaseModel):

    class Meta(GenreCategoryBaseModel.Meta):

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(GenreCategoryBaseModel):

    class Meta(GenreCategoryBaseModel.Meta):

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=LIMIT_NAME)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.PositiveIntegerField(
        'Год произведения',
        validators=[
            year_validator
        ]
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='reviews_unique',
                fields=['title', 'author'],
            )
        ]

    def __str__(self):
        return f'{self.author} - {self.title} - {self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author} к отзыву {self.review.id}'
