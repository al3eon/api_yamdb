from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from users.constants import LIMIT_EMAIL, LIMIT_USERNAME
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import username_validator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=LIMIT_USERNAME,
        required=True,
        validators=[username_validator]
    )
    email = serializers.EmailField(
        max_length=LIMIT_EMAIL,
        required=True
    )

    def validate(self, data):
        username = data['username']
        email = data['email']

        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username).email != email:
                raise serializers.ValidationError(
                    {'email': 'Email не соответствует пользователю'}
                )

        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).username != username:
                raise serializers.ValidationError(
                    {'username': 'Username не соответствует пользователю'}
                )

        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()

        send_mail(
            'Код подтверждения для YaMDb',
            f'Ваш код подтверждения: {user.confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError('Неверный код подтверждения')
        return {'token': str(AccessToken.for_user(user))}


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate(self, attrs):
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, attrs):
        return super().validate(attrs)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')

    def get_rating(self, obj):
        return obj.rating

    def validate(self, attrs):
        return super().validate(attrs)


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        # Чтобы запрос без жанров не прошел валидацию надо добавить два параметра для этого поля:
        # allow_null и allow_empty. Значением для обоих будет False.
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = request.user
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'review', 'author', 'pub_date')
