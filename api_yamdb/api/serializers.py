from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from api.validators import username_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        extra_kwargs = {
            'role': {'required': False}
        }

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                _('Использовать имя "me" в качестве username запрещено')
            )
        return username_validator(value)


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=[username_validator]
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        email_error = _('Email не соответствует пользователю')
        username_error = _('Username не соответствует пользователю')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError({'email': email_error})

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError({'username': username_error})

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=[username_validator]
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LIMIT_CODE,
        required=True
    )

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            confirmation_code=data.get('confirmation_code')
        )

        if not user:
            raise serializers.ValidationError(
                _('Неверная комбинация username и кода подтверждения')
            )

        return {
            'token': str(AccessToken.for_user(user))
        }
