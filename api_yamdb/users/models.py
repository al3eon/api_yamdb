from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import LIMIT_EMAIL, LIMIT_USERNAME, OUTPUT_LENGTH
from api.validators import username_validator


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        'Имя пользователя',
        max_length=LIMIT_USERNAME,
        unique=True,
        help_text=f'Обязательное поле. Не более {LIMIT_USERNAME} символов. '
                  f'Только буквы, цифры и @/./+/-/_.',
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует!',
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=LIMIT_EMAIL,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует!',
        },
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role in Role.values),
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        help_text='Расскажите немного о себе'
    )
    first_name = models.CharField(
        'Имя',
        max_length=LIMIT_USERNAME,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LIMIT_USERNAME,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:OUTPUT_LENGTH]
