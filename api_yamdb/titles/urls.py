from django.urls import include, path
from rest_framework import routers

from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('', include(router.urls))
]
