from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from titles.permission import IsAdminOrReadOnly
from titles.models import Genre, Category, Title
from titles.serializers import (TitleSerializer,
                                GenreSerializer, CategorySerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
