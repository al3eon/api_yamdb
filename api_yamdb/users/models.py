from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.validators import username_validator


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username = models.CharField(
        _('Имя пользователя'),
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        help_text=_(
            'Обязательное поле. Не более %(limit)s символов. '
            'Только буквы, цифры и @/./+/-/_.'
        ) % {'limit': settings.LIMIT_USERNAME},
        validators=[username_validator],
        error_messages={
            'unique': _('Пользователь с таким именем уже существует!'),
        },
    )
    email = models.EmailField(
        _('Электронная почта'),
        max_length=settings.LIMIT_EMAIL,
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким email уже существует!'),
        },
    )
    role = models.CharField(
        _('Роль'),
        max_length=max(len(role) for role in Role.values),
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
        help_text=_('Расскажите немного о себе')
    )
    confirmation_code = models.CharField(
        _('Код подтверждения'),
        max_length=settings.LIMIT_CODE,
        blank=True,
        null=True,
        help_text=_('Код для подтверждения регистрации')
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=settings.LIMIT_USERNAME,
        blank=True
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=settings.LIMIT_USERNAME,
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

    def clean(self):
        if self.username.lower() == 'me':
            raise ValidationError(
                _('Использовать имя пользователя "%(username)s" запрещено')
                % {'username': 'me'}
            )
        super().clean()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('username',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me"
            )
        ]

    def __str__(self):
        return self.username[:settings.OUTPUT_LENGTH]
