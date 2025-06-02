from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import signup, token, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include([
        path('auth/signup/', signup, name='signup'),
        path('auth/token/', token, name='token'),
        path('', include(router.urls)),
        path('', include('titles.urls')),
        path('', include('reviews.urls'))
    ]))
]
