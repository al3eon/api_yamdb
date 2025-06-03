from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# Это не универсальный переводчик. Данная функция умеет работать только с заранее заданными фразами.
# Их можно дополнять, но нет необходимости делать это в рамках учебного проекта.
# Давайте просто уберем.

from api.validators import username_validator
# Заведем в каждом приложении файл constants.py для хранения констант.
# Не надо все складывать в settings.py
from api_yamdb.settings import (
    LIMIT_CODE, LIMIT_EMAIL, LIMIT_USERNAME, OUTPUT_LENGTH
)


class User(AbstractUser):
    # Хороший выбор инструмента для создания вариантов значения для поля role
    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username = models.CharField(
        _('Имя пользователя'),
        max_length=LIMIT_USERNAME,
        unique=True,
        help_text=_(
            'Обязательное поле. Не более %(limit)s символов. '
            'Только буквы, цифры и @/./+/-/_.'
        # Используем f-строку для формирования help_text.
        # Форматирование через % считается устаревшим (наследие второго питона).
        ) % {'limit': LIMIT_USERNAME},
        validators=[username_validator],
        error_messages={
            'unique': _('Пользователь с таким именем уже существует!'),
        },
    )
    email = models.EmailField(
        _('Электронная почта'),
        max_length=LIMIT_EMAIL,
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким email уже существует!'),
        },
    )
    role = models.CharField(
        _('Роль'),
        # Хороший способ задать лимит длины поля.
        max_length=max(len(role) for role in Role.values),
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
        help_text=_('Расскажите немного о себе')
    )
    # Лишнее поле. Вы используете default_token_generator. Этот инструмент позволяет не хранить данные в БД.
    # Механизм схож с механизмом JWT-токенов - в токен зашифровывается часть данных пользователя
    # (его id) и некоторая мета-информация. Проверка валидности осуществляется через default_token_generator.check_token
    confirmation_code = models.CharField(
        _('Код подтверждения'),
        max_length=LIMIT_CODE,
        blank=True,
        null=True,
        help_text=_('Код для подтверждения регистрации')
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=LIMIT_USERNAME,
        blank=True
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=LIMIT_USERNAME,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    # Супер!
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('username',)

    def __str__(self):
        return self.username[:OUTPUT_LENGTH]
