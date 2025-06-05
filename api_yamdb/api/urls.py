from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, signup, TitleViewSet,
    token, UserViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

nested_router = DefaultRouter()
nested_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
nested_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include([
        path('auth/signup/', signup, name='signup'),
        path('auth/token/', token, name='token'),
        path('', include(router.urls)),
        path('', include(nested_router.urls)),
    ]))
]
