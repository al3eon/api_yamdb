import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import LIMIT_NAME, LIMIT_SLUG
from titles.models import Category, Genre


def username_validator(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя "me" использовать нельзя!')

    invalid_chars = re.sub(r'^[\w.@+-]+\Z', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы: {invalid_chars}'
        )
    return value


def slug_validator_genre(value):
    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError('Не правильный формат Slug')

    if len(value) > LIMIT_SLUG:
        raise ValidationError(
            ('Slug может содержать максимум 50 символов')
        )

    queryset = Genre.objects.filter(slug=value)

    if queryset.exists():
        raise ValidationError('Такой slug уже существует для жанра.')


def slug_validator_category(value):
    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError('Не правильный формат Slug')

    if len(value) > LIMIT_SLUG:
        raise ValidationError(
            ('Slug может содержать максимум 50 символов')
        )

    queryset = Category.objects.filter(slug=value)

    if queryset.exists():
        raise ValidationError('Такой slug уже существует для жанра.')


def name_validator(value):
    if len(value) > LIMIT_NAME:
        raise ValidationError('Слишком большое имя')
    return value
