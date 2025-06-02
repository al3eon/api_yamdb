from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, token

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')  # Добавлен basename

urlpatterns = [
    path('v1/', include([
        path('auth/signup/', signup, name='signup'),
        path('auth/token/', token, name='token'),
        path('', include(router.urls)),
        path('', include('titles.urls')),
        path('', include('reviews.urls'))
    ]))
]
