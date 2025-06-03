from django.db import models
from django.db.models import Avg

# Заведем в каждом приложении файл constants.py для хранения констант.
# Не надо все складывать в settings.py
from api_yamdb.settings import LIMIT_NAME, LIMIT_SLUG


# Модели категорий и жанров очень похожи. Чтобы не дублировать настройки полей, создадим абстрактную модель,
# где прописать эти настройки, и будем наследоваться от нее.
class Genre(models.Model):
    # Это поле тоже сделаем уникальным.
    # Будет странно, если у нас окажется два жанра с одинаковым названием, но разными слагами.
    name = models.CharField('Название жанра', max_length=LIMIT_NAME)
    slug = models.SlugField('Слаг', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        # Во всех моделях задаем сортировку по умолчанию (ordering).
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
    # Для текстовых полей не стоит использовать null=True. Это породит двойственность для отсутствия значения -
    # будет возможна и пустая строка и Null. Вот тут в документации об этом говорится.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#null
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    # Подберем более подходящий тип поля. Значения в данном поле являются маленькими числами.
    # В соответствии со спецификацией значение данного поля не может превышать значение текущего года.
    # Добавим тут соответствующую валидацию (понадобится валидирующая функция, которую привяжем к полю через параметр validators).
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

    # Такой подход породит множество запросов в БД (отдельный запрос для каждого элемента QuerySet).
    # Нужно изменить подход: добавьте атрибут rating для всех элементов QuerySet путем его аннотирования во вью.
    # Документация для annotate и для Avg
    # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate
    # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#avg
    @property
    def rating(self):
        return self.reviews.aggregate(Avg('score'))['score__avg']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    # При использовании ManuToManyField Django автоматически создает промежуточную таблицу.
    # Руками ее прописывать не надо, если нет необходимости дополнить ее какими-то полями.
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
