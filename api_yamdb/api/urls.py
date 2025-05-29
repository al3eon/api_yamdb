from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, token

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(router.urls)),
]
