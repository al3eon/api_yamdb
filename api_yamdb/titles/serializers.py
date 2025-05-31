from rest_framework import serializers

from titles.models import Genre, Category, Title
from api.validators import (slug_validator_genre, slug_validator_category,
                            name_validator)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,  # Для обработки списка жанров
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[name_validator])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating'
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        return obj.rating


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(validators=[slug_validator_genre])

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        validators=[slug_validator_category]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')
