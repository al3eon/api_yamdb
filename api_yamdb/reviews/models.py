import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import LIMIT_NAME, LIMIT_SLUG, MAX_SCORE, MIN_SCORE


class BaseModel(models.Model):
    # Название стоит уточнить. Это не базовая модель, т.к. от нее наследуются не все модели, а лишь часть.
    # Лучше в названии указать какие поля она добавляет или для каких моделей является базовой.
    name = models.CharField('Название', unique=True, max_length=LIMIT_NAME)
    slug = models.SlugField('Слаг', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        abstract = True


class Genre(BaseModel):

    class Meta:
        # Сортировку и метод __str__ тоже убираем в абстрактную модель.
        # Чтобы сортировка работала надо будет в 22 и 35 строках явно унаследоваться от BaseModel.Meta
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(BaseModel):

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=LIMIT_NAME)
    # Для текстовых полей не стоит использовать null=True.
    # Это породит двойственность для отсутствия значения - будет возможна и пустая строка и Null.
    # Вот тут в документации об этом говорится.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#null
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.PositiveSmallIntegerField(
        'Год произведения',
        validators=[
            # Минимальное значение ограничивать не надо.
            # В нашем проекте мы можем добавлять любые произведения, в том числе созданные до нашей эры.
            # Могут пригодиться отрицательные числа (тип поля, соответственно, тоже надо поправить).
            MinValueValidator(1000),
            # Так будет работать некорректно. Текущий год будет вычислен при запуске приложения
            # и далее обновляться не будет. Чтобы это поправить, вместо MaxValueValidator надо создать функцию
            # с соответствующей проверкой, которую привязать в параметр validators
            MaxValueValidator(datetime.datetime.now().year)
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
