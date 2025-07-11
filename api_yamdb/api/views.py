from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrStaffOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    TokenSerializer,
    UserEditSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['=username']
    filterset_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserEditSerializer
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects
        .select_related('category')
        .prefetch_related('genre')
        .annotate(rating=Avg('reviews__score'))
        .order_by('name', 'year')
    )
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleCreateSerializer


class BaseGenreCategoryViewSet(mixins.DestroyModelMixin,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(BaseGenreCategoryViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class CategoryViewSet(BaseGenreCategoryViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class BaseReviewCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(BaseReviewCommentViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all().order_by('-pub_date')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(BaseReviewCommentViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all().order_by('-pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
