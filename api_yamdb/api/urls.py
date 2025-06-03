from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, token
from reviews.urls import urlpatterns as reviews_urls
from titles.urls import urlpatterns as titles_urls

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include([
        path('auth/signup/', signup, name='signup'),
        path('auth/token/', token, name='token'),
        path('', include(router.urls)),
        path('', include(titles_urls)),
        path('', include(reviews_urls)),
    ]))
]
