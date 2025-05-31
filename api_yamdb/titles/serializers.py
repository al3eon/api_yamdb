from rest_framework import serializers

from titles.models import Genre, Category, Title
from api.validators import (slug_validator_genre, slug_validator_category,
                            name_validator)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    #rating = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[name_validator])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        return obj.rating

    def get_genres(self, obj):
        """Возвращаем список жанров с name и slug"""
        return [
            {
                'name': genre.name,
                'slug': genre.slug
            }
            for genre in obj.genres.all()
        ]

    def to_representation(self, instance):
        """Преобразуем вывод, чтобы category возвращалась как объект"""
        representation = super().to_representation(instance)
        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug
        }

        return representation


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
