from rest_framework import serializers

from api.validators import (
    name_validator, slug_validator_category, slug_validator_genre
)
from titles.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(validators=[slug_validator_genre])

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        validators=[slug_validator_category]
    )
    name = serializers.CharField(
        validators=[name_validator]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_validator])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')

    def get_rating(self, obj):
        return obj.rating


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    name = serializers.CharField(validators=[name_validator])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
